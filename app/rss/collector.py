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
bad_whitespace = re.compile(r"\s+")

def tidy(text: str) -> str:
    """
    Strip HTML, fix mojibake, normalise whitespace, drop junk endings like [â€¦]
    """
    # 1. strip tags
    txt = BeautifulSoup(text, "html.parser").get_text(" ", strip=True)

    # 2. fix mojibake
    txt = fix_text(txt, normalization='NFC')

    # 3. remove [â€¦] or [...]
    txt = re.sub(r"\[.*?\]$", "", txt)  # ← kill trailing [anything]
    txt = re.sub(r"[.…]{3,}$", "", txt)  # ← kill trailing ..., ……

    # 4. normalize spaces
    txt = bad_whitespace.sub(" ", txt).strip()

    #5. final clean
    txt = txt.encode('ascii', 'ignore').decode('ascii')  # strip out broken characters like â


    return txt
def fetch_latest(limit: int = 200, feed_urls: List[str] = None) -> List[Dict]:
    articles: List[Dict] = []

    # fallback to global if none passed
    urls = feed_urls if feed_urls else RSS_FEEDS

    for url in urls:
        print(f"Fetching from: {url}")
        try:
            response = requests.get(url, headers=HEADERS, timeout=10)
            parsed = feedparser.parse(response.content)
            print(f"Found {len(parsed.entries)} entries")

            for entry in parsed.entries:
                clean_summary = tidy(entry.get("summary", ""))
                clean_title = tidy(entry.get("title", ""))

                article = {
                    "title": clean_title,
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


if __name__ == "__main__":
    feeds = get_feed_configs()
    print("Fetched Feeds:", feeds)
    print(f"Total feeds fetched: {len(feeds)}")