from guardian_api import fetch_guardian_articles, get_api_key
from message_broker import send_message_to_sqs
import logging

# import argparse
# import json
# import os


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def run(search_term: str, date_from: str, queue_url: str, logger: None):
    """ """

    logger.info("Fetching Guardian API Key...")
    guardian_api_key = get_api_key(logger=logger)

    logger.info(f"Fetching articles for {search_term}")
    articles = fetch_guardian_articles(
        guardian_api_key=guardian_api_key,
        search_term=search_term,
        date_from=date_from,
        logger=logger,
    )

    if not articles:
        logger.info("No articles found.")
        return

    logger.info(f"Sending {len(articles)} articles to broker...")
    send_message_to_sqs(articles, queue_url, logger=logger)
    logger.info("Pipeline complete.")


def lambda_handler(event, context):
    """
    Expected event format:
    {
        "search_term": "machine learning",
        "date_from": "2023-01-01",
        "queue_url": etc
    }
    """
    logger.info(f"Received event {event}...")
    search_term = event.get("search_term")
    date_from = event.get("date_from")
    queue_url = event.get("queue_url")

    run(
        search_term=search_term,
        date_from=date_from,
        queue_url=queue_url,
        logger=logger,
    )


# For testing
if __name__ == "__main__":
    lambda_handler()
