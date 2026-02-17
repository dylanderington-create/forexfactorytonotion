import os
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

NOTION_TOKEN = os.environ["NOTION_TOKEN"]
DATABASE_ID  = "30abc939-7ab2-80bb-b951-fd1f33054d04"

HEADERS_NOTION = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type":  "application/json",
    "Notion-Version": "2022-06-28",
}
HEADERS_FF = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def get_week_range():
    today = datetime.utcnow().date()
    monday = today - timedelta(days=today.weekday())
    sunday = monday + timedelta(days=6)
    return monday, sunday

def fetch_ff_events():
    monday, _ = get_week_range()
    url = f"https://www.forexfactory.com/calendar?week={monday.strftime('%b%d.%Y').lower()}"
    resp = requests.get(url, headers=HEADERS_FF, timeout=15)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    events = []
    current_date = None

    for row in soup.select("tr.calendar__row"):
        date_cell = row.select_one("td.calendar__date span")
        if date_cell and date_cell.get_text(strip=True):
            try:
                raw = date_cell.get_text(strip=True)
                current_date = datetime.strptime(
                    f"{raw} {datetime.utcnow().year}", "%a %b %d %Y"
                ).date()
            except ValueError:
                pass

        impact_el = row.select_one("td.calendar__impact span")
        if not impact_el:
            continue
        if "high" not in " ".join(impact_el.get("class", [])).lower():
            continue

        currency_el = row.select_one("td.calendar__currency")
        currency = currency_el.get_text(strip=True) if currency_el else ""
        if currency != "USD":
            continue

        name_el  = row.select_one("td.calendar__event span.calendar__event-title")
        name     = name_el.get_text(strip=True) if name_el else ""
        time_el  = row.select_one("td.calendar__time")
        time_str = time_el.get_text(strip=True) if time_el else ""

        forecast_el = row.select_one("td.calendar__forecast")
        forecast    = forecast_el.get_text(strip=True) if forecast_el else ""

        previous_el = row.select_one("td.calendar__previous")
        previous    = previous_el.get_text(strip=True) if previous_el else ""

        if current_date and name:
            events.append({
                "name":     name,
                "date":     current_date.isoformat(),
                "time":     time_str,
                "currency": currency,
                "forecast": forecast,
                "previous": previous,
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
    print("🔍 Fetching Forex Factory events...")
    events = fetch_ff_events()
    print(f"📅 Found {len(events)} High-Impact USD events this week.")
    if events:
        print("🗑  Clearing old entries...")
        clear_existing_entries()
        print("📝 Writing to Notion...")
        write_to_notion(events)
        print("🎉 Done!")
    else:
        print("⚠️  No events found.")
