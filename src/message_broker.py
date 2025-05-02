from typing import List, Dict
import boto3
import json


def send_message_to_sqs(messages: List[Dict], queue_url: str, logger=None):
    """
    Sends a list of article messages to the specified SQS queue.

    Args:
        messages List[Dict]: List of article dictionaries to send.
        queue_url str: Full URL of the SQS queue.
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
