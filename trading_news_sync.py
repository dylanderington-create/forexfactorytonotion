import os
import requests
from datetime import datetime, timedelta, timezone
from dateutil import parser as date_parser

NOTION_TOKEN = os.environ["NOTION_TOKEN"]
DATABASE_ID  = "ef6933a2-9055-4dab-a66a-5d7a2f81da46"

HEADERS_NOTION = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type":  "application/json",
    "Notion-Version": "2022-06-28",
}

HEADERS_WEB = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
}

def get_week_range():
    today = datetime.now(timezone.utc).date()
    monday = today - timedelta(days=today.weekday())
    sunday = monday + timedelta(days=6)
    return monday, sunday

def fetch_events():
    monday, sunday = get_week_range()

    # Versuche mehrere Quellen
    urls = [
        "https://cdn-nfs.faireconomy.media/ff_calendar_thisweek.json",
        "https://nfs.faireconomy.media/ff_calendar_thisweek.json",
    ]

    raw = None
    for url in urls:
        try:
            print(f"📡 Trying: {url}")
            resp = requests.get(url, headers=HEADERS_WEB, timeout=20)
            print(f"   Status: {resp.status_code}")
            if resp.status_code == 200:
                raw = resp.json()
                print(f"   ✅ Got {len(raw)} events")
                break
        except Exception as e:
            print(f"   ❌ Failed: {e}")
            continue

    if not raw:
        print("⚠️ All sources failed.")
        return []

    events = []
    for ev in raw:
        if ev.get("country") != "USD":
            continue
        if ev.get("impact") != "High":
            continue

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

    print(f"✅ {len(events)} High-Impact USD events for this week")
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
        print("⚠️ No events found.")
