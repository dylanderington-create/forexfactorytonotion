import os
import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
import re

NOTION_TOKEN = os.environ["NOTION_TOKEN"]
DATABASE_ID  = "30abc939-7ab2-8052-a440-000bf01fba7a"

HEADERS_NOTION = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type":  "application/json",
    "Notion-Version": "2022-06-28",
}

# High-Impact USD Keywords (Forex Factory "red" events)
HIGH_IMPACT_KEYWORDS = [
    "Non-Farm", "NFP", "CPI", "FOMC", "Federal Reserve", "Fed Rate",
    "GDP", "Unemployment", "Retail Sales", "PCE", "PPI", "ISM",
    "Consumer Price", "Producer Price", "Durable Goods", "Trade Balance",
    "Jobless Claims", "Housing Starts", "Powell", "Interest Rate Decision",
    "Core CPI", "Core PCE", "ADP", "PMI"
]

def get_week_range():
    today = datetime.now(timezone.utc).date()
    monday = today - timedelta(days=today.weekday())
    sunday = monday + timedelta(days=6)
    return monday, sunday

def fetch_rss_events():
    """Fetch from TradingEconomics RSS Feed"""
    url = "https://tradingeconomics.com/rss/calendar.aspx"
    params = {"c": "united states"}
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/rss+xml, application/xml, text/xml, */*",
    }

    print(f"📡 Fetching TradingEconomics RSS...")
    resp = requests.get(url, params=params, headers=headers, timeout=20)
    print(f"   Status: {resp.status_code}")
    resp.raise_for_status()

    root = ET.fromstring(resp.content)
    channel = root.find("channel")
    items = channel.findall("item") if channel else root.findall(".//item")
    print(f"   Found {len(items)} raw items")

    monday, sunday = get_week_range()
    events = []

    for item in items:
        title = item.findtext("title", "").strip()
        pub_date_str = item.findtext("pubDate", "").strip()
        description = item.findtext("description", "").strip()

        # Parse date
        try:
            # RSS pubDate format: "Mon, 17 Feb 2026 14:30:00 GMT"
            pub_date = datetime.strptime(pub_date_str, "%a, %d %b %Y %H:%M:%S %Z")
            pub_date = pub_date.replace(tzinfo=timezone.utc)
        except Exception:
            continue

        event_date = pub_date.date()

        # Only current week
        if not (monday <= event_date <= sunday):
            continue

        # Only High-Impact Keywords
        is_high_impact = any(kw.lower() in title.lower() for kw in HIGH_IMPACT_KEYWORDS)
        if not is_high_impact:
            continue

        # MEZ = UTC+1
        mez_time = pub_date + timedelta(hours=1)

        # Extract forecast/previous from description if available
        forecast = ""
        previous = ""
        if description:
            fore_match = re.search(r"forecast[:\s]+([0-9\.\-\+%KMB]+)", description, re.IGNORECASE)
            prev_match = re.search(r"previous[:\s]+([0-9\.\-\+%KMB]+)", description, re.IGNORECASE)
            if fore_match:
                forecast = fore_match.group(1)
            if prev_match:
                previous = prev_match.group(1)

        events.append({
            "title": title,
            "date": event_date.isoformat(),
            "time": mez_time.strftime("%H:%M") + " MEZ",
            "currency": "USD",
            "impact": "🔴 High",
            "forecast": forecast,
            "previous": previous,
        })

    print(f"   ✅ {len(events)} High-Impact events for this week")
    return events

def clear_existing_entries():
    """Delete all existing entries in the Notion DB"""
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    has_more = True
    next_cursor = None

    while has_more:
        payload = {"page_size": 100}
        if next_cursor:
            payload["start_cursor"] = next_cursor
        resp = requests.post(url, headers=HEADERS_NOTION, json=payload)
        data = resp.json()

        for page in data.get("results", []):
            page_id = page["id"]
            requests.patch(
                f"https://api.notion.com/v1/pages/{page_id}",
                headers=HEADERS_NOTION,
                json={"archived": True}
            )

        has_more = data.get("has_more", False)
        next_cursor = data.get("next_cursor")

def write_to_notion(events):
    url = "https://api.notion.com/v1/pages"
    for ev in events:
        payload = {
            "parent": {"database_id": DATABASE_ID},
            "properties": {
                "Name": {"title": [{"text": {"content": ev["title"]}}]},
                "Datum": {"date": {"start": ev["date"]}},
                "Zeit": {"rich_text": [{"text": {"content": ev["time"]}}]},
                "Währung": {"select": {"name": ev["currency"]}},
                "Impact": {"select": {"name": ev["impact"]}},
                "Prognose": {"rich_text": [{"text": {"content": ev["forecast"]}}]},
                "Vorher": {"rich_text": [{"text": {"content": ev["previous"]}}]},
            }
        }
        resp = requests.post(url, headers=HEADERS_NOTION, json=payload)
        if resp.status_code == 200:
            print(f"   ✅ {ev['date']} {ev['time']} — {ev['title']}")
        else:
            print(f"   ❌ Failed: {ev['title']} — {resp.text}")

if __name__ == "__main__":
    monday, sunday = get_week_range()
    print(f"📅 Week: {monday} → {sunday}")

    events = fetch_rss_events()

    if events:
        print("🗑  Clearing old entries...")
        clear_existing_entries()
        print("📝 Writing to Notion...")
        write_to_notion(events)
        print("🎉 Done!")
    else:
        print("⚠️  No High-Impact events found for this week.")
