from guardian_api import fetch_guardian_articles, get_api_key
from message_broker import send_message_to_sqs
import logging
import argparse
import os


# import json


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def run(search_term: str, date_from: str, queue_url: str, logger: None):
    """
    Executes the end-to-end data streaming pipeline.

    Retrieves the Guardian API key from AWS Secrets Manager, fetches articles
    matching the given search term and date, and publishes the results to an
    AWS SQS message broker. Logs each step for observability.

    Args:
        search_term (str):
            The keyword or phrase to search for in Guardian articles.
        date_from (str):
            The starting date (YYYY-MM-DD) to filter articles from.
        queue_url (str):
            The URL of the AWS SQS queue to publish messages to.
        logger (logging.Logger):
            Logger instance for emitting informational and error messages.

    Returns:
        None
    """
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
    try:
        send_message_to_sqs(articles, queue_url, logger=logger)
    except Exception as error:
        logger.error(f"Pipeline failed while sending to SQS: {error}")
        return
    logger.info("Pipeline complete.")


def lambda_handler(event, context):
    """
    AWS Lambda entry point for invoking the Guardian data streaming pipeline.

    This function is triggered by an AWS event,
    extracts parameters from the event payload,
    initiates the article ingestion,
    publishing process via the 'run' function.

    Expected event payload format:
        {
            "search_term": "machine learning",
            "date_from": "2023-01-01",
            "queue_url":
                "https://sqs.eu-west-2.amazonaws.com/123456789012/guardian_content"
        }

    Args:
        event (dict):
            The event payload passed by the Lambda trigger.
        context (object):
            AWS Lambda context object containing metadata.

    Returns:
        None
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
    # Local cli logger 
    logger = logging.getLogger("cli")
    logging.basicConfig(level=logging.INFO)

    # Can be run locally for testing
    parser = argparse.ArgumentParser(
        description="Guardian Stream articles to SQS"
    )
    parser.add_argument(
        "--search_term",
        help="Search term for Guardian articles",
        required=True,
    )
    parser.add_argument(
        "--date_from", help="Start date (YYYY-MM-DD)", default=None
    )
    parser.add_argument(
        "--queue_url", help="SQS Queue URL", default=None, required=True
    )


    args = parser.parse_args()
    queue_url = args.queue_url or os.getenv("QUEUE_URL")
    if not queue_url:
        print("Error: Not queue_url provided. Use --queue_url or set QUEUE_URL environment variable.")
        exit(1)
    
    run(args.search_term, args.date_from, queue_url, logger=logger)
