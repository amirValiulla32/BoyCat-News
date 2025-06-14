from app.rss.supabase_client import supabase
from app.rss.utils import get_best_logo_url, download_image_bytes, upload_to_supabase_storage
def save_articles_to_supabase(articles, feed):
    existing_urls_response = supabase.table("campaigns_rss_items").select("url").execute()
    existing_urls = set(item["url"] for item in existing_urls_response.data)

    for article in articles:
        if article["url"] in existing_urls:
            print(f" Skipping duplicate: {article['url']}")
            continue

        record = {
            "title": article["title"],
            "url": article["url"],
            "published_at": article["published_at"],
            "source": article["source"],
            "summary": article["summary"],
            "campaign_id": feed["campaign_id"],
            "brand_id": feed.get("brand_id"),  
            "feed_id": feed["id"],             
        }

        try:
            supabase.table("campaigns_rss_items").upsert(record).execute()

            # Fetch the article ID just inserted
            try:
                inserted_article = supabase.table("campaigns_rss_items").select("id").eq("url", article["url"]).single().execute()
                article_id = inserted_article.data["id"]

                logo_url = get_best_logo_url(feed["url"], article["url"])
                print(f"Logo URL: {logo_url}") 
                image_bytes = download_image_bytes(logo_url)
                if not image_bytes:
                    print(" Failed to download image from:", logo_url)
                else:
                    print(" Image bytes downloaded.") 

                if image_bytes:
                    logo_path = upload_to_supabase_storage(image_bytes, f"{article_id}.png")
                    print("Upload result (logo_path):", logo_path)
                    print(f"Uploaded to: {logo_path}")
                if logo_path:
                    update_result = supabase.table("campaigns_rss_items").update({
                    "logo_url": logo_url,
                    "logo_path": logo_path
                    }).eq("id", article_id).execute()
                    print("Update result:", update_result)  # 👈 Log the DB update
                else:
                    print(" Upload failed.")

                    # Update the article with logo_url and logo_path
                    supabase.table("campaigns_rss_items").update({
                        "logo_url": logo_url,
                        "logo_path": logo_path
                    }).eq("id", article_id).execute()

            except Exception as e:
                print(" Error handling logo storage:", e)

        except Exception as e:
            print(" Error inserting record:", e)
        existing_urls.add(article["url"])

    print(" Finished inserting articles (duplicates skipped)")