import os
import json
import logging
from config_loader import load_config_from_yaml
from scrapers.jobs_scraper import scrape_jobs
from scrapers.weather_scraper import scrape_weather
from scrapers.tvsporten_scraper import scrape_tvsporten
from scrapers.tilbuds_scraper import scrape_tilbud
from scrapers.news_scraper import scrape_news

def scrape_data(urls, data_type, scraper):
    """
    Scrapes data from a list of URLs using the provided scraper function.
    """
    all_data = []
    for url in urls:
        try:
            logging.debug(f"Scraping {data_type} data from {url}")
            data = scraper(url)
            if data:
                all_data.extend(data)
        except Exception as e:
            logging.error(f"Failed to scrape {url}: {str(e)}")
    return all_data

def write_data_to_file(output_file, all_data):
    """
    Writes the scraped data to a JSON file.
    """
    try:
        with open(output_file, "w") as json_file:
            json.dump(all_data, json_file, indent=1, ensure_ascii=False)
        logging.info(f"Successfully saved scraped data to {output_file}")
    except OSError as e:
        logging.error(f"Failed to write to {output_file}: {str(e)}")

def main():
    logging.basicConfig(level=logging.DEBUG)
    config_files = [
        "configs/jobs.yml",
        "configs/weather.yml",
        "configs/tvsporten.yml",
        "configs/tilbud.yml",
        "configs/news.yml",
    ]
    
    scraping_functions = {
        "jobs": scrape_jobs,
        "weather": scrape_weather,
        "tvsporten": scrape_tvsporten,
        "tilbud": scrape_tilbud,
        "news": scrape_news,
    }

    for config_file in config_files:
        config = load_config_from_yaml(config_file)
        urls = config["urls"]
        data_type = config["data_type"]
        output_file = config["output_file"]

        if data_type not in scraping_functions:
            raise ValueError(f"Unknown data type: {data_type}")

        scraper = scraping_functions[data_type]
        all_data = scrape_data(urls, data_type, scraper)
        write_data_to_file(output_file, all_data)

if __name__ == "__main__":
    main()
