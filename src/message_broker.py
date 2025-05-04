from typing import List, Dict
import boto3
import json


def send_message_to_sqs(messages: List[Dict], queue_url: str, logger=None):
    """
    Sends a list of article messages to the specified AWS SQS queue.

    Iterates through each article in the provided list and sends it as a JSON-formatted
    message to the given queue URL. Logs each successful message send using the
    provided logger.

    Args:
        messages (List[Dict]): A list of article dictionaries to send to the message broker.
        queue_url (str): The full URL of the AWS SQS queue where messages will be published.
        logger (logging.Logger, optional): Logger instance for emitting informational messages.

    Returns:
        None
    """
    sqs = boto3.client("sqs", region_name="eu-west-2")

    for message in messages:
        response = sqs.send_message(
            QueueUrl=queue_url, MessageBody=json.dumps(message)
        )
        logger.info(
            f"Message sent to SQS with ID: {response.get('MessageId')}"
        )


# For testing
if __name__ == "__main__":
    send_message_to_sqs()
