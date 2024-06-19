import feedparser
import requests

def fetch_rss_feed(url):
    response = requests.get(url)
    response.raise_for_status()
    return feedparser.parse(response.content)

def parse_feed(feed):
    news_items = []
    for entry in feed.entries:
        news_item = {
            'title': entry.title if 'title' in entry else 'No title',
            'description': entry.description if 'description' in entry else 'No description',
            'link': entry.link if 'link' in entry else 'No link',
            'published': entry.published if 'published' in entry else 'No published date',
            'guid': entry.guid if 'guid' in entry else 'No GUID',
            'category': entry.category if 'category' in entry else 'No category'
        }
        # Optional: add media content if available
        if 'media_content' in entry:
            news_item['media_content'] = entry.media_content[0]['url']
        news_items.append(news_item)
    return news_items

def scrape_news(url):
    all_news_items = []
    try:
        feed = fetch_rss_feed(url)
        news_items = parse_feed(feed)
        all_news_items.extend(news_items)
    except Exception as e:
        print(f"Error fetching or parsing feed {url}: {e}")

    return all_news_items
