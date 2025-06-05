from app.rss.supabase_client import supabase

def save_articles_to_supabase(articles: list):
    if not articles:
        print("No articles to insert.")
        return

    try:
        # Upsert into the table on unique key 'url'
        response = supabase.table("campaigns_rss_items") \
            .upsert(articles, on_conflict="url") \
            .execute()

        print(f"Inserted {len(response.data)} new articles.")
    except Exception as e:
        print("Error inserting articles into Supabase:", e)