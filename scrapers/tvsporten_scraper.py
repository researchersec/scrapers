import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pytz
import re


def scrape_tvsporten(url):
    # Get the current date and time in CEST timezone
    cest = pytz.timezone("Europe/Berlin")
    now = datetime.now(cest)
    current_date = now.strftime("%Y-%m-%d")
    print(f"Current date (CEST): {current_date}")
    print(f"Current time (CEST): {now.strftime('%H:%M')}")

    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    matches = []

    # Find all divs with the class "day event_day__js"
    day_divs = soup.find_all("div", class_="day event_day__js")

    for day in day_divs:
        date_attr = day.get("data-date", "")
        if date_attr != current_date:
            print(f"Skipping date: {date_attr}")
            continue
        print(f"Processing date: {date_attr}")

        match_divs = day.find_all("div", class_="match-info")

        for match in match_divs:
            match_time_element = match.find("div", class_="match-time")
            if not match_time_element:
                print("No match time element found, skipping...")
                continue

            match_time_str = match_time_element.text.strip()
            print(f"Found match time: {match_time_str}")

            try:
                match_time = datetime.strptime(match_time_str, "%H:%M").replace(
                    year=now.year, month=now.month, day=now.day, tzinfo=cest
                )
            except ValueError:
                print(f"Error parsing match time: {match_time_str}, skipping...")
                continue

            if match_time <= now:
                print(
                    f"Match time {match_time_str} is before current time, skipping..."
                )
                continue

            match_detail = match.find_next_sibling("div", class_="match-detail")
            if not match_detail:
                print("No match detail element found, skipping...")
                continue

            title_element = match_detail.find("h3")
            title = title_element.text.strip() if title_element else "N/A"
            print(f"Match title: {title}")

            category_element = match_detail.find("p")
            category_text = (
                category_element.get_text(separator=" ").strip()
                if category_element
                else "N/A"
            )

            # Remove everything after ' · ' (dot + space) using regex
            category_cleaned = re.sub(r"\s*·.*", "", category_text)

            print(f"Match category: {repr(category_cleaned)}")

            channels = []
            for channel in match_detail.find_all("li"):
                img = channel.find("img")
                if img:
                    channel_name = img.get("alt", "N/A")
                    if channel_name not in [
                        "Danske Spil Live Odds",
                        "VBet Live Odds",
                        "Expekt Live Odds",
                        "BET 365 STREAM",
                    ]:
                        channels.append(
                            {"name": channel_name, "logo_url": img.get("src", "")}
                        )

            if len(channels) == 0:
                print("No valid channels found, skipping match...")
                continue

            match_info = {
                "match": title,
                "category": category_cleaned,
                "time": match_time_str,
                "date": current_date,
                "channels": channels,
            }

            matches.append(match_info)
            print(f"Match added: {match_info}")

    print(f"Total matches found: {len(matches)}")
    return matches


if __name__ == "__main__":
    url = "https://www.tvsporten.dk/"
    matches = scrape_tvsporten(url)
    print(matches)
