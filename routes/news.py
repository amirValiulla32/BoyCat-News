from fastapi import APIRouter, Query
from typing import List

from rss_parser.collector import fetch_latest
from rss_parser.filter import keyword_filter

router = APIRouter(prefix="/news")

@router.get("/")
def get_news(
    campaign: str = Query(..., min_length=2),
    brand: str | None = Query(None),
    limit: int = 10,
):
    """Return filtered news for a campaign (and optional brand)."""
    # 1. basic keyword list
    keywords: List[str] = [campaign]
    if brand:
        keywords.append(brand)

    # 2. fetch & filter
    raw_articles = fetch_latest(limit=50)          # pull more than we need
    articles = keyword_filter(raw_articles, keywords, max_results=limit)
    ##articles = raw_articles[:limit]

    # 3. shape response
    return {
        "campaign": campaign,
        "brand": brand,
        "keywords": keywords,
        "count": len(articles),
        "articles": articles,
    }
@router.get("/debug")
def debug_rss():
    from rss_parser.collector import fetch_latest
    articles = fetch_latest(limit=10)
    return {"articles": articles}
