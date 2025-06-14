# run_parser.py
from db import get_feed_configs
from app.rss.collector import fetch_latest
from app.rss.filter import keyword_filter
from save_articles_to_supabase import save_articles_to_supabase
from app.rss.utils import get_best_logo_url

CAMPAIGN_KEYWORDS = ["gaza"]
BRAND_KEYWORDS = ["starbucks"]
MAX_RESULTS = 5

def main():
    feed_configs = get_feed_configs()
    print("Loaded Feeds:", [f["url"] for f in feed_configs])

    for feed in feed_configs:
        url = feed["url"]

        raw_articles = fetch_latest(limit=50, feed_urls=[url])
        keywords = CAMPAIGN_KEYWORDS + BRAND_KEYWORDS
        filtered = keyword_filter(raw_articles, keywords, max_results=MAX_RESULTS)

        for article in filtered:
            logo_url = get_best_logo_url(feed["url"], article["url"])
            print(f"{'title:':12} {article['title']}")
            print(f"{'url:':12} {article['url']}")
            print(f"{'published at:':12} {article['published_at']}")
            print(f"{'source:':12} {article['source']}")
            print(f"{'summary:':12} {article['summary']}")
            print(f"{'logo_url:':12} {logo_url}")
            print("-" * 50)
        if filtered:
            save_articles_to_supabase(filtered, feed)


if __name__ == "__main__":
    main()
