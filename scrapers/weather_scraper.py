import requests
import logging


def scrape_weather(url):
    logging.basicConfig(level=logging.DEBUG)

    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    headers = {"User-Agent": user_agent}

    try:
        logging.debug(f"Fetching weather data from {url}")
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        weather_data = response.json()
        current_data = weather_data.get("CurrentData", {})
        temperature = current_data.get("temperature", "N/A")
        sky_text = current_data.get("skyText", "N/A")
        humidity = current_data.get("humidity", "N/A")
        wind_text = current_data.get("windText", "N/A")
        weatherstuff = []
        weatherstuff.append(
            {
                "temperature": temperature,
                "sky_text": sky_text,
                "humidity": humidity,
                "wind_text": wind_text,
            }
        )
        return weatherstuff
    except requests.exceptions.RequestException as e:
        logging.error(f"Request error: {e}")
        return None
    except ValueError as e:
        logging.error(f"Error parsing JSON: {e}")
        return None
