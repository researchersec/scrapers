import os
import json
import logging
from config_loader import load_config_from_yaml
from scrapers.jobs_scraper import scrape_jobs
from scrapers.weather_scraper import scrape_weather
from scrapers.tvsporten_scraper import scrape_tvsporten
from scrapers.tilbuds_scraper import scrape_tilbud
from scrapers.news_scraper import scrape_news


def main():
    logging.basicConfig(level=logging.DEBUG)
    config_files = [
        # region specific
        "configs/region-nordjylland-jobs.yml",
        "configs/region-nordjylland-weather.yml",
        # general
        "configs/tvsporten.yml",
        "configs/tilbud.yml",
        "configs/news.yml",
    ]

    for config_file in config_files:
        config = load_config_from_yaml(config_file)
        urls = config["urls"]
        data_type = config["data_type"]
        output_file = config["output_file"]
        all_data = []

        for url in urls:
            if data_type == "jobs":
                logging.debug(f"Scraping jobs data from {url}")
                data = scrape_jobs(url)
            elif data_type == "weather":
                logging.debug(f"Scraping weather data from {url}")
                data = scrape_weather(url)
            elif data_type == "tvsporten":
                logging.debug(f"Scraping TV sport data from {url}")
                data = scrape_tvsporten(url)
            elif data_type == "tilbud":
                logging.debug(f"Scraping tilbuds data from {url}")
                data = scrape_tilbud(url)
            elif data_type == "news":
                logging.debug(f"Scraping news data from {url}")
                data = scrape_news(url)
            else:
                raise ValueError(f"Unknown data type: {data_type}")

            if data:
                all_data.extend(data)

        with open(output_file, "w") as json_file:
            json.dump(all_data, json_file, indent=1, ensure_ascii=False)


if __name__ == "__main__":
    main()
