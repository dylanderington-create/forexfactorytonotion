import os
import requests
from datetime import datetime, timedelta

NOTION_TOKEN = os.environ["NOTION_TOKEN"]
DATABASE_ID  = "30abc939-7ab2-80bb-b951-fd1f33054d04"

HEADERS_NOTION = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type":  "application/json",
    "Notion-Version": "2022-06-28",
}

def get_week_range():
    today = datetime.utcnow().date()
    monday = today - timedelta(days=today.weekday())
    sunday = monday + timedelta(days=6)
    return monday, sunday

def fetch_events():
    monday, sunday = get_week_range()
    url = "https://economic-calendar.tradingview.com/events"
    params = {
        "from":       f"{monday.isoformat()}T00:00:00.000Z",
        "to":         f"{sunday.isoformat()}T23:59:59.000Z",
        "countries":  "US",
        "importances": "high",
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Origin":     "https://www.tradingview.com",
        "Referer":    "https://www.tradingview.com/",
    }
    resp = requests.get(url, params=params, headers=headers, timeout=15)
    resp.raise_for_status()
    data = resp.json()

    events = []
    for ev in data.get("result", []):
        if ev.get("importance") != "high":
            continue
        if ev.get("country") != "US":
            continue

        dt = datetime.strptime(ev["date"][:19], "%Y-%m-%dT%H:%M:%S")
        # Zeitzone UTC → MEZ (+1) bzw. MESZ (+2)
        # Einfach als UTC ausgeben, du siehst dann selbst
        date_str = dt.date().isoformat()
        time_str = dt.strftime("%H:%M") + " UTC"

        events.append({
            "name":     ev.get("title", ""),
            "date":     date_str,
            "time":     time_str,
            "currency": "USD",
            "forecast": str(ev.get("forecast", "") or ""),
            "previous": str(ev.get("previous", "") or ""),
        })

    return events

def clear_existing_entries():
    monday, sunday = get_week_range()
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    resp = requests.post(url, headers=HEADERS_NOTION, json={"filter": {"and": [
        {"property": "Datum", "date": {"on_or_after":  monday.isoformat()}},
        {"property": "Datum", "date": {"on_or_before": sunday.isoformat()}},
    ]}})
    resp.raise_for_status()
    pages = resp.json().get("results", [])
    for page in pages:
        requests.patch(
            f"https://api.notion.com/v1/pages/{page['id']}",
            headers=HEADERS_NOTION,
            json={"archived": True}
        )
    print(f"Cleared {len(pages)} old entries.")

def write_to_notion(events):
    for ev in events:
        r = requests.post(
            "https://api.notion.com/v1/pages",
            headers=HEADERS_NOTION,
            json={
                "parent": {"database_id": DATABASE_ID},
                "properties": {
                    "Name":     {"title":    [{"text": {"content": ev["name"]}}]},
                    "Datum":    {"date":     {"start": ev["date"]}},
                    "Zeit":     {"rich_text":[{"text": {"content": ev["time"]}}]},
                    "Währung":  {"select":   {"name": ev["currency"]}},
                    "Impact":   {"select":   {"name": "🔴 High"}},
                    "Prognose": {"rich_text":[{"text": {"content": ev["forecast"]}}]},
                    "Vorher":   {"rich_text":[{"text": {"content": ev["previous"]}}]},
                },
            }
        )
        print(f"{'✅' if r.status_code == 200 else '❌'} {ev['date']} {ev['time']} — {ev['name']}")

if __name__ == "__main__":
    print("🔍 Fetching TradingView Economic Calendar...")
    events = fetch_events()
    print(f"📅 Found {len(events)} High-Impact USD events this week.")
    if events:
        print("🗑  Clearing old entries...")
        clear_existing_entries()
        print("📝 Writing to Notion...")
        write_to_notion(events)
        print("🎉 Done!")
    else:
        print("⚠️  No events found.")
