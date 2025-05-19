import feedparser
import requests
from typing import List, Dict

RSS_FEEDS = [
    "https://www.middleeastmonitor.com/feed",
    "https://mondoweiss.net/feed",
    "https://electronicintifada.net/rss.xml",
    "https://www.aljazeera.com/tag/palestine/rss",
    "https://theintercept.com/feed/?rss"
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Boycat NewsBot)"
}

def fetch_latest(limit: int = 20) -> List[Dict]:
    print("💣 fetch_latest() is running")
    articles = []

    for url in RSS_FEEDS:
        print(f"🌐 Fetching from: {url}")
        try:
            response = requests.get(url, headers=HEADERS, timeout=10)
            parsed = feedparser.parse(response.content)
            print(f"📄 Found {len(parsed.entries)} entries")

            for entry in parsed.entries:
                articles.append({
                    "title": entry.get("title", ""),
                    "url": entry.get("link", ""),
                    "published_at": entry.get("published", ""),
                    "source": parsed.feed.get("title", "unknown"),
                    "summary": entry.get("summary", ""),
                })

        except Exception as e:
            print(f"❌ Error fetching {url} → {e}")
            continue

    print(f"✅ Total articles fetched: {len(articles)}")
    return articles[:limit]
