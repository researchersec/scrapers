import os
import json
import requests
import shutil
import yfinance as yf
from datetime import datetime

# Load Discord webhook URL from environment variable
DISCORD_WEBHOOK_URL = os.getenv("WHURL")
if not DISCORD_WEBHOOK_URL:
    raise ValueError("Discord webhook URL is not set. Check your GitHub Secrets.")

# File paths
CURRENT_FILE = "jobs.json"
BACKUP_FILE = "jobs_backup.json"
NEWS_SENT_FILE = "news_sent.json"

def load_json(file_path):
    """Load JSON data from a file."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_backup(current_file, backup_file):
    """Create a backup of the current JSON file."""
    shutil.copy(current_file, backup_file)

def get_new_entries(old_data, new_data):
    """Identify new entries by comparing old and new data."""
    old_jobs = {job['job_URL'] for job in old_data}
    return [job for job in new_data if job['job_URL'] not in old_jobs]

def send_discord_notification(job):
    """Send a job notification to Discord."""
    message = {
        "content": f"**New Job Posted!**\n**Title:** {job['title']}\n**Company:** {job['company']}\n**Location:** {job['location']}\n[Apply Now]({job['job_URL']})"
    }
    response = requests.post(DISCORD_WEBHOOK_URL, json=message)
    if response.status_code == 204:
        print(f"Notification sent for job: {job['title']}")
    else:
        print(f"Failed to send notification: {response.status_code}")

def notify_new_jobs():
    """Check for new jobs and notify Discord."""
    old_data = load_json(BACKUP_FILE)
    new_data = load_json(CURRENT_FILE)
    new_entries = get_new_entries(old_data, new_data)

    for job in new_entries:
        send_discord_notification(job)

    save_backup(CURRENT_FILE, BACKUP_FILE)

def send_intc_news():
    """Fetch and send new INTC news articles to Discord."""
    ticker = yf.Ticker("INTC")
    news = ticker.news

    if not news:
        print("No news found for INTC.")
        return

    try:
        with open(NEWS_SENT_FILE, "r", encoding="utf-8") as f:
            sent_ids = set(json.load(f))
    except (FileNotFoundError, json.JSONDecodeError):
        sent_ids = set()

    new_articles = [article for article in news if article['uuid'] not in sent_ids]

    for article in new_articles:
        title = article.get("title", "No Title")
        publisher = article.get("publisher", "Unknown Publisher")
        link = article.get("link", "#")
        summary = article.get("summary", "")

        message = {
            "content": f"📰 **INTC News Alert**\n**Title:** {title}\n**Source:** {publisher}\n{summary}\n[Read More]({link})"
        }

        response = requests.post(DISCORD_WEBHOOK_URL, json=message)
        if response.status_code == 204:
            print(f"Sent news: {title}")
        else:
            print(f"Failed to send news: {response.status_code}")

    # Update the record of sent news
    sent_ids.update(article["uuid"] for article in new_articles)
    with open(NEWS_SENT_FILE, "w", encoding="utf-8") as f:
        json.dump(list(sent_ids), f, indent=2)

# Run the functions
if __name__ == "__main__":
    notify_new_jobs()
    send_intc_news()
