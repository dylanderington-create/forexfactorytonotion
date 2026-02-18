import os
import requests
import csv
import io
from datetime import datetime, timedelta, timezone

NOTION_TOKEN      = os.environ["NOTION_TOKEN"]
ALPHA_VANTAGE_KEY = os.environ["ALPHA_VANTAGE_KEY"]
DATABASE_ID       = "ef6933a2-9055-4dab-a66a-5d7a2f81da46"

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
    print(f"📡 Fetching Alpha Vantage Economic Calendar...")
    print(f"   Week: {monday} → {sunday}")

    url = "https://www.alphavantage.co/query"
    params = {
        "function": "ECONOMIC_CALENDAR",
        "horizon":  "3month",
        "apikey":   ALPHA_VANTAGE_KEY,
    }

    resp = requests.get(url, params=params, timeout=20)
    print(f"   Status: {resp.status_code}")
    resp.raise_for_status()

    reader = csv.DictReader(io.StringIO(resp.text))
    events = []

    for row in reader:
        country  = row.get("country", "").strip()
        impact   = row.get("impact", "").strip().lower()
        date_str = row.get("date", "").strip()

        if country != "United States":
            continue
        if impact != "high":
            continue

        try:
            event_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except Exception:
            continue

        if not (monday <= event_date <= sunday):
            continue

        time_str = row.get("time", "").strip()
        if time_str and time_str != "-":
            try:
                t = datetime.strptime(time_str, "%H:%M")
                mez = t + timedelta(hours=1)
                time_display = mez.strftime("%H:%M") + " MEZ"
            except Exception:
                time_display = time_str
        else:
            time_display = "Ganztägig"

        events.append({
            "title":    row.get("event", row.get("title", "")).strip(),
            "date":     event_date.isoformat(),
            "time":     time_display,
            "currency": "USD",
            "impact":   "🔴 High",
            "forecast": row.get("forecast", "").strip(),
            "previous": row.get("previous", "").strip(),
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
        print("⚠️  No High-Impact USD events found for this week.")
