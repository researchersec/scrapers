import json
import requests
import shutil

# Discord Webhook URL
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/YOUR_WEBHOOK_ID/YOUR_WEBHOOK_TOKEN"

# File paths
CURRENT_FILE = "jobs.json"
BACKUP_FILE = "jobs_backup.json"

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
    # Load current and backup data
    old_data = load_json(BACKUP_FILE)
    new_data = load_json(CURRENT_FILE)

    # Identify new entries
    new_entries = get_new_entries(old_data, new_data)

    # Send notifications for new entries
    for job in new_entries:
        send_discord_notification(job)

    # Update the backup file
    save_backup(CURRENT_FILE, BACKUP_FILE)

# Run the function after the scraper is complete
if __name__ == "__main__":
    notify_new_jobs()
