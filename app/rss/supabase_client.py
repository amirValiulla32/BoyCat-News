from supabase import create_client
from dotenv import load_dotenv
import os

load_dotenv()  # Load from .env

SUPABASE_URL = os.getenv("SB_URL")
SUPABASE_KEY = os.getenv("SB_SERVICE_ROLE_KEY")  

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Missing Supabase credentials in environment variables")



supabase = create_client(SUPABASE_URL, SUPABASE_KEY)