import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import requests
from io import BytesIO
import os
from supabase import create_client
from uuid import uuid4
from dotenv import load_dotenv

load_dotenv()  
SUPABASE_URL = os.getenv("SB_URL")
SUPABASE_KEY = os.getenv("SB_SERVICE_ROLE_KEY")
SUPABASE_BUCKET = os.getenv("SB_BUCKET", "boycat-production")  

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def upload_to_supabase_storage(image_bytes: bytes, record_id: int) -> str:
    """
    Upload image bytes to Supabase storage bucket and return public URL.
    Uses record_id as the filename in logos directory.
    """
    if not image_bytes:
        print("[upload_to_supabase_storage] No image bytes provided.")
        return None

    try:
        ext = "png"
        file_path = f"post-newsletter-media/logos/{record_id}.{ext}"
        bucket_path = f"{file_path}"  # path inside post-newsletter-media bucket

        res = supabase.storage.from_(SUPABASE_BUCKET).upload(
            bucket_path,
            image_bytes,
            {
                "content-type": "image/png",
                "x-upsert": "true"
            }
        )

        # Handle both dict (legacy) and UploadResponse object
        if isinstance(res, dict) and res.get("error"):
            print(f"[upload_to_supabase_storage] Upload error: {res['error']['message']}")
            return None
        if hasattr(res, 'error') and res.error:
            print(f"[upload_to_supabase_storage] Upload error: {res.error.message}")
            return None

        public_url = f"{SUPABASE_URL}/storage/v1/object/public/{SUPABASE_BUCKET}/{bucket_path}"
        return public_url

    except Exception as e:
        print(f"[upload_to_supabase_storage] Exception: {e}")
        return None
    
def get_domain(feed_url):
    return urlparse(feed_url).netloc

def try_rss_image(feed_url):
    try:
        response = requests.get(feed_url, timeout=5)
        soup = BeautifulSoup(response.content, 'xml')
        image_tag = soup.find('image')
        if image_tag and image_tag.find('url'):
            return image_tag.find('url').text.strip()
    except:
        return None

def try_html_icon(article_url):
    try:
        response = requests.get(article_url, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        icon_links = soup.find_all("link", rel=lambda x: x and 'icon' in x.lower())
        for link in icon_links:
            href = link.get("href")
            if href:
                return urljoin(article_url, href)
    except:
        return None

def try_clearbit(feed_url):
    domain = get_domain(feed_url)
    return f"https://logo.clearbit.com/{domain}"

def try_favicon(feed_url):
    domain = get_domain(feed_url)
    return f"https://{domain}/favicon.ico"

def get_best_logo_url(feed_url, article_url):
    return (
        try_rss_image(feed_url) or
        try_html_icon(article_url) or
        try_clearbit(feed_url) or
        try_favicon(feed_url)
    )

def download_image_bytes(logo_url: str) -> bytes:
    try:
        response = requests.get(logo_url, timeout=10)
        response.raise_for_status()
        return response.content
    except Exception as e:
        print(f"Failed to download image: {e}")
        return None