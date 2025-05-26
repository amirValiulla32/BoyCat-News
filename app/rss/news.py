from fastapi import APIRouter, Query
from typing import List
import json
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from parser.app.rss.collector import fetch_latest
from parser.app.rss.filter import keyword_filter
from fastapi.responses import Response
from parser.app.auth import verify_api_key
from fastapi import Depends
from fastapi.security import APIKeyHeader


router = APIRouter(
    prefix="/news",
    dependencies=[Depends(verify_api_key)]
)

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

    # 3. shape response
    response_data = {
        "campaign": campaign,
        "brand": brand,
        "keywords": keywords,
        "count": len(articles),
        "articles": articles,
    }
    
    return Response(
        content=json.dumps(jsonable_encoder(response_data), indent=2),
        media_type="application/json"
    )
@router.get("/debug")
def debug_rss():
    from parser.app.rss.collector import fetch_latest
    articles = fetch_latest(limit=10)
    return {"articles": articles}
