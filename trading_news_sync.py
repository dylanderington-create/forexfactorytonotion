import os
import requests
from datetime import datetime, timedelta, timezone
import dateutil.parser as date_parser

NOTION_TOKEN = os.environ["NOTION_TOKEN"]
DATABASE_ID  = "ef6933a2-9055-4dab-a66a-5d7a2f81da46"

HEADERS_NOTION = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type":  "application/json",
    "Notion-Version": "2022-06-28",
}

def get_week_range():
    today = datetime.now(timezone.utc).date()
    monday = today - timedelta(days=today.weekday())
    sunday = monday + timedelta(days=6)
    return monday, sunday

def fetch_events():
    monday, sunday = get_week_range()
    print(f"📡 Fetching Forex Factory Calendar JSON...")

    url = "https://cdn-nfs.faireconomy.media/ff_calendar_thisweek.json"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    }

    resp = requests.get(url, headers=headers, timeout=20)
    print(f"   Status: {resp.status_code}")
    resp.raise_for_status()

    raw = resp.json()
    print(f"   Total events in feed: {len(raw)}")

    events = []
    for ev in raw:
        # Nur USD High Impact
        if ev.get("country") != "USD":
            continue
        if ev.get("impact") != "High":
            continue

        # Datum parsen
        try:
            dt_parsed = date_parser.parse(ev["date"])
            event_date = dt_parsed.date()
        except Exception:
            continue

        # UTC → MEZ (+1)
        if dt_parsed.tzinfo:
            mez = dt_parsed + timedelta(hours=1)
        else:
            mez = dt_parsed
        time_display = mez.strftime("%H:%M") + " MEZ"

        events.append({
            "title":    ev.get("title", "").strip(),
            "date":     event_date.isoformat(),
            "time":     time_display,
            "currency": "USD",
            "impact":   "🔴 High",
            "forecast": ev.get("forecast", "") or "",
            "previous": ev.get("previous", "") or "",
        })

    print(f"   ✅ {len(events)} High-Impact USD events found")
    return events

def clear_existing_entries():
    print("🗑  Clearing old entries...")
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
            requests.patch(
                f"https://api.notion.com/v1/pages/{page['id']}",
                headers=HEADERS_NOTION,
                json={"archived": True}
            )
        has_more = data.get("has_more", False)
        next_cursor = data.get("next_cursor")

def write_to_notion(events):
    print("📝 Writing to Notion...")
    url = "https://api.notion.com/v1/pages"
    for ev in events:
        payload = {
            "parent": {"database_id": DATABASE_ID},
            "properties": {
                "Name":     {"title": [{"text": {"content": ev["title"]}}]},
                "Datum":    {"date": {"start": ev["date"]}},
                "Zeit":     {"rich_text": [{"text": {"content": ev["time"]}}]},
                "Währung":  {"select": {"name": ev["currency"]}},
                "Impact":   {"select": {"name": ev["impact"]}},
                "Prognose": {"rich_text": [{"text": {"content": ev["forecast"]}}]},
                "Vorher":   {"rich_text": [{"text": {"content": ev["previous"]}}]},
            }
        }
        resp = requests.post(url, headers=HEADERS_NOTION, json=payload)
        if resp.status_code == 200:
            print(f"   ✅ {ev['date']} {ev['time']} — {ev['title']}")
        else:
            print(f"   ❌ {ev['title']} — {resp.text}")

if __name__ == "__main__":
    monday, sunday = get_week_range()
    print(f"📅 Week: {monday} → {sunday}")
    events = fetch_events()
    if events:
        clear_existing_entries()
        write_to_notion(events)
        print("🎉 Done!")
    else:
        print("⚠️  No High-Impact USD events found.")
