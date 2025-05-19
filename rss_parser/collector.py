import requests
import feedparser
from bs4 import BeautifulSoup
from typing import List, Dict
import unicodedata
import html 
from ftfy import fix_text   
import re


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
def clean(summary: str) -> str:
    text = fix_text(summary)                     # fixes mojibake
    text = re.sub(r"\s+", " ", text).strip()     # normalise whitespace
    return text

def fetch_latest(limit: int = 20) -> List[Dict]:
    print(" fetch_latest() is running")
    articles: List[Dict] = []

    for url in RSS_FEEDS:
        print(f" Fetching from: {url}")
        try:
            response = requests.get(url, headers=HEADERS, timeout=10)
            parsed = feedparser.parse(response.content)
            print(f" Found {len(parsed.entries)} entries")

            for entry in parsed.entries:
                raw_summary   = entry.get("summary", "")
                stripped_html = BeautifulSoup(raw_summary, "html.parser").get_text(" ", strip=True)
                clean_summary = clean(stripped_html)

                article = {
                    "title": entry.get("title", ""),
                    "url": entry.get("link", ""),
                    "published_at": entry.get("published", ""),
                    "source": parsed.feed.get("title", "unknown"),
                    "summary": clean_summary
                }

                articles.append(article)

        except Exception as e:
            print(f" Error fetching {url} → {e}")
            continue

    print(f" Total articles fetched: {len(articles)}")
    return articles[:limit]
