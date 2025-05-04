from typing import Optional, List, Dict
import boto3
import requests


GUARDIAN_API_URL = "https://content.guardianapis.com/search"


def get_api_key(secret_name="guardian_api_key", logger=None):
    """
    Retrieves the Guardian API key from AWS Secrets Manager.

    Uses secret name to fetch the API key stored in Secrets Manager.
    Returns the secret string if successful, or None if retrieval fails.

    Args:
        secret_name (str, optional):
            The name of secret in AWS Secrets Manager.
        logger (logging.Logger, optional):
            Logger instance for logging info and error messages.

    Returns:
        str or None:
            The secret string (API key) if found; None otherwise.
    """
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
    """
    Fetches a list of articles from The Guardian API based on a search term.

    Makes an HTTP GET request to the Guardian API using the API key and
    optional date filter, returning up to 'page_size' results.

    Args:
        guardian_api_key (str):
            The API key for accessing the Guardian Content API.
        search_term (str):
            The term to search for in Guardian articles.
        date_from (Optional[str], optional):
            Date string (YYYY-MM-DD) to filter results from. Defaults to None.
        page_size (int, optional):
            The maximum number of articles to return. Defaults to 10.
        logger (logging.Logger, optional):
            Logger instance for logging debug and error messages.

    Returns:
        List[Dict]: A list of dictionaries containing the following fields:
            - webPublicationDate (str):
                Publication timestamp of the article.
            - webTitle (str):
                Title of the article.
            - webUrl (str):
                URL link to the article.
            - content_preview (str):
                Truncated preview of the article body (max 1000 chars).
    """
    if not guardian_api_key:
        logger.error(f"Guardian api key empty: {guardian_api_key}")
        return []

    params = {
        "q": search_term,
        "api-key": guardian_api_key,
        "page-size": page_size,
        "order-by": "newest",
        "show-fields": "all",
    }

    if date_from:
        params["from-date"] = date_from

    logger.info("Calling api...")
    logger.info(f"params {params}")
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
