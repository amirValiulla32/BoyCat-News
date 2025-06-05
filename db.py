from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()  # Make sure .env vars load

SUPABASE_URL = os.getenv("SB_URL")
SUPABASE_KEY = os.getenv("SB_SERVICE_ROLE_KEY")
print("URL:", SUPABASE_URL)
print("KEY:", SUPABASE_KEY[:8], "...")  # Truncate for safety
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_feed_configs():
    response = supabase.table("campaigns_rss_feeds").select("*").eq("active", True).execute()
    return response.data
