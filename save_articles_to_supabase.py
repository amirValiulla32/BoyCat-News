from app.rss.supabase_client import supabase

def save_articles_to_supabase(articles, feed):
    for article in articles:
        record = {
            "title": article["title"],
            "url": article["url"],
            "published_at": article["published_at"],
            "source": article["source"],
            "summary": article["summary"],
            "campaign_id": feed["campaign_id"],
            "brand_id": feed.get("brand_id"),  # optional
            "feed_id": feed["id"],             # this avoids the NOT NULL error
        }

        try:
            supabase.table("campaigns_rss_items").upsert(record).execute()
        except Exception as e:
            print(" Error inserting record:", e)