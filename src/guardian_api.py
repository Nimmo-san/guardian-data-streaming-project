from typing import Optional, List, Dict
import boto3
import requests


GUARDIAN_API_URL = "https://content.guardianapis.com/search"


def get_api_key(secret_name="guardian_api_key", logger=None):
    """ """
    logger.info(f"Calling secrets manager for API Key -> {secret_name}...")
    client = boto3.client("secretsmanager", region_name="eu-west-2")
    try:
        response = client.get_secret_value(SecretId=secret_name)
        logger.info("Found API Key")
        return response.get("SecretString")
    except Exception as e:
        logger.error(f"Failed to retrieve secret: {e}")
        return


def fetch_guardian_articles(
    guardian_api_key: str,
    search_term: str,
    date_from: Optional[str] = None,
    page_size: int = 10,
    logger=None,
) -> List[Dict]:
    """ """
    if not guardian_api_key:
        logger.error(f"Guardian api key empty: {guardian_api_key}")

    params = {
        "q": search_term,
        "api-key": guardian_api_key,
        "page-size": page_size,
        "order-by": "newest",
        "show-fields": "all",
    }

    if date_from:
        params["from-date"] = date_from

    logger.info(f"Calling api with params {params}")
    response = requests.get(GUARDIAN_API_URL, params=params)

    if response.status_code != 200:
        logger.error(
            f"Received response - status code: {response.status_code}"
        )

    logger.info(f"Response status code - {response.status_code}")
    data = response.json()
    articles = data.get("response", {}).get("results", [])

    simplified_articles = []
    for article in articles:
        preview = article.get("fields", {}).get("bodyText", "")
        content_preview = preview[:1000] if preview else ""

        simplified_articles.append(
            {
                "webPublicationDate": article.get("webPublicationDate"),
                "webTitle": article.get("webTitle"),
                "webUrl": article.get("webUrl"),
                "content_preview": content_preview,
            }
        )

    logger.info("Returning formatted data...")
    return simplified_articles


# For testing
if __name__ == "__main__":
    api_key = get_api_key()
    fetch_guardian_articles(
        api_key, search_term="finance", date_from="2025-01-01"
    )
