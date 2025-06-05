# run_parser.py
from db import get_feed_configs
from app.rss.collector import fetch_latest
from app.rss.filter import keyword_filter
from save_articles_to_supabase import save_articles_to_supabase

CAMPAIGN_KEYWORDS = ["gaza"]
BRAND_KEYWORDS = ["starbucks"]
MAX_RESULTS = 5

def get_rss_feed_urls():
    configs = get_feed_configs()
    return [feed["url"] for feed in configs if feed.get("url")]

def main():
    feed_urls = get_rss_feed_urls()
    print("Loaded Feeds:", feed_urls)

    raw_articles = fetch_latest(limit=50, feed_urls=feed_urls)
    keywords = CAMPAIGN_KEYWORDS + BRAND_KEYWORDS
    filtered = keyword_filter(raw_articles, keywords, max_results=MAX_RESULTS)
    for article in filtered:
        print(f"{'title:':12} {article['title']}")
        print(f"{'url:':12} {article['url']}")
        print(f"{'published at:':12} {article['published_at']}")
        print(f"{'source:':12} {article['source']}")
        print(f"{'summary:':12} {article['summary']}")
        print("-" * 50)


if __name__ == "__main__":
    main()
feed_configs = get_feed_configs()

