from typing import Optional, List, Dict
from dotenv import load_dotenv
import logging
import requests
import os
from pprint import pprint

load_dotenv()

logger = logging.getLogger()
logger.setLevel(logging.INFO)

GUARDIAN_API_URL = "https://content.guardianapis.com/search"


def fetch_guardian_articles(
        search_term: str,
        date_from: Optional[str] = None,
        page_size: int = 10
    ) -> List[Dict]:

    guardian_api = os.getenv("GUARDIAN_API_KEY")
    if not guardian_api:
        logger.error(f"Guardian api key empty: {guardian_api}")

    params = {
        "q": search_term,
        "api-key": guardian_api,
        "page-size": page_size,
        "order-by": "newest",
        "show-fields": "all"
    }

    if date_from:
        params["from-date"] = date_from

    logger.info("Calling api...")
    response = requests.get(GUARDIAN_API_URL, params=params)

    if response.status_code != 200:
        logger.error(f"Received response - status code: {response.status_code}")

    logger.info(f"Response status code - {response.status_code}")
    data = response.json()
    articles = data.get("response", {}).get("results", [])


    simplified_articles = []
    for article in articles:
        preview = article.get("fields", {}).get("bodyText", "")
        content_preview = preview[:1000] if preview else ""

        simplified_articles.append({
            "webPublicationDate": article.get("webPublicationDate"),
            "webTitle": article.get("webTitle"),
            "webUrl": article.get("webUrl"),
            "content_preview": content_preview
        })

    logger.info("Returning formatted data...")
    pprint(simplified_articles)
    return simplified_articles

fetch_guardian_articles(search_term="finance", date_from="2025-01-01")