from unittest.mock import patch, MagicMock
from src.message_broker import send_message_to_sqs


class TestMessageBroker:
    @patch("src.message_broker.boto3.client")
    def test_send_message_to_sqs(self, mock_boto_client):
        # Mock the logger
        logger = MagicMock()

        # Prepare a dummy SQS client
        mock_sqs = MagicMock()
        mock_boto_client.return_value = mock_sqs
        mock_sqs.send_message.return_value = {"MessageId": "abc-123"}

        # Sample message and test queue URL
        test_messages = [
            {
                "webPublicationDate": "2023-01-01T10:00:00Z",
                "webTitle": "Sample",
                "webUrl": "https://example.com",
                "content_preview": "Example content",
            }
        ]
        queue_url = (
            "https://sqs.eu-west-2.amazonaws.com/123456789012/guardian_content"
        )

        # Call the function
        send_message_to_sqs(test_messages, queue_url, logger)

        # Assert send_message was called once
        assert mock_sqs.send_message.call_count == 1

        # Checking logger was called
        logger.info.assert_called_with("Message sent to SQS with ID: abc-123")
