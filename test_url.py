import requests
from bs4 import BeautifulSoup


def fetch_html_content(url):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")

        html_content = soup.prettify()
        print(html_content)
    else:
        print(f"Failed to retrieve {url}. Status code: {response.status_code}")


if __name__ == "__main__":
    url = "https://www.dmi.dk/danmark/regionaludsigter-dk"
    fetch_html_content(url)
