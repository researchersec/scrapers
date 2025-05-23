import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import base64

def scrape_tilbud(url):
    # Send request to get the page
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Find all app-data tags and look for the one with offers
    app_data_tags = soup.find_all("app-data")
    offer_data = None
    for tag in app_data_tags:
        data_key = tag.get("data-key")
        if data_key:
            try:
                # Decode the data-key to check if it contains offers
                decoded_key = base64.b64decode(data_key).decode("utf-8")
                key_json = json.loads(decoded_key)
                if isinstance(key_json, list) and key_json[0] == "offers":
                    offer_data = json.loads(tag.text)
                    break
            except (base64.binascii.Error, json.JSONDecodeError, UnicodeDecodeError):
                continue

    if not offer_data:
        print("No offer data found in app-data tags.")
        return []

    tilbud = []

    for item in offer_data.get("data", []):
        # Extract fields
        link = f"/{item.get('business', {}).get('slugs', [''])[0]}?publication={item.get('publicationPublicId', '')}&offer={item.get('publicId', '')}"
        price = str(item.get("price", ""))
        currency = item.get("currencyCode", "DKK")
        valid_from = item.get("validFrom", "")
        valid_until = item.get("validUntil", "")
        image = item.get("image", "")

        try:
            if valid_from:
                valid_from_dt = datetime.strptime(valid_from, "%Y-%m-%dT%H:%M:%S+0000")
                valid_from = valid_from_dt.strftime("%d-%m-%Y")
        except ValueError:
            valid_from = ""

        try:
            if valid_until:
                valid_until_dt = datetime.strptime(valid_until, "%Y-%m-%dT%H:%M:%S+0000")
                valid_until = valid_until_dt.strftime("%d-%m-%Y")
        except ValueError:
            valid_until = ""

        tilbud.append(
            {
                "link": link,
                "price": price,
                "currency": currency,
                "valid_from": valid_from,
                "valid_until": valid_until,
                "image": image
            }
        )

    return tilbud
