import requests
from bs4 import BeautifulSoup
from datetime import datetime

def scrape_tilbud(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    offer_items = soup.find_all(
        "li", class_="OfferList__OfferListItem-sc-bj82vg-1 eBZAOf"
    )
    tilbud = []

    for item in offer_items:
        link = item.find("a")["href"]
        price = item.find("meta", itemprop="price")["content"]
        currency = item.find("meta", itemprop="priceCurrency")["content"]
        valid_from = item.find("meta", itemprop="validFrom")["content"]
        valid_until = item.find("meta", itemprop="validThrough")["content"]
        image = item.find("img")["src"] 

        valid_from = datetime.strptime(valid_from, "%Y-%m-%dT%H:%M:%S.%fZ").strftime(
            "%d-%m-%Y"
        )
        valid_until = datetime.strptime(valid_until, "%Y-%m-%dT%H:%M:%S.%fZ").strftime(
            "%d-%m-%Y"
        )

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
