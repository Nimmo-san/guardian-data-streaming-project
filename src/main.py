from guardian_api import fetch_guardian_articles
from message_broker import send_message_to_sqs
import logging
# import argparse
# import json
# import os


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def run(search_term: str, date_from: str, queue_url: str):
    """ """
    logger.info(f"Fetching articles for {search_term}")

    articles = fetch_guardian_articles(search_term, date_from, logger=logger)

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

    run(search_term, date_from, queue_url)


# For testing
if __name__ == "__main__":
    pass
