from typing import List, Dict

def keyword_filter(
    articles: List[Dict],
    keywords: List[str],
    max_results: int = 10,
) -> List[Dict]:
    """Return only articles whose title OR summary contains any keyword."""
    lowered = [k.lower() for k in keywords]
    filtered = [
        a for a in articles
        if any(k in (a["title"] + " " + a["summary"]).lower() for k in lowered)
    ]
    return filtered[:max_results]
