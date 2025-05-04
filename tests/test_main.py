from unittest.mock import patch, MagicMock
from main import run, lambda_handler

# import pytest


class TestMain:
    @patch("main.get_api_key")
    @patch("main.fetch_guardian_articles")
    @patch("main.send_message_to_sqs")
    def test_run_with_articles(self, mock_send, mock_fetch, mock_get_key):
        mock_logger = MagicMock()
        mock_get_key.return_value = "test_api_key"
        mock_fetch.return_value = [
            {
                "webPublicationDate": "2023-01-01",
                "webTitle": "Test Title",
                "webUrl": "https://example.com",
                "content_preview": "Preview content",
            }
        ]

        run("test topic", "2023-01-01", "https://sqs-url", mock_logger)

        mock_fetch.assert_called_once_with(
            guardian_api_key="test_api_key",
            search_term="test topic",
            date_from="2023-01-01",
            logger=mock_logger,
        )
        mock_send.assert_called_once()

    # @pytest.mark.skip
    @patch("main.logger")
    @patch("main.run")
    def test_lambda_handler(self, mock_run, mock_logger):
        event = {
            "search_term": "AI",
            "date_from": "2023-01-01",
            "queue_url": "https://sqs-url",
        }

        lambda_handler(event, None)
        # from unittest.mock import ANY
        mock_run.assert_called_once_with(
            search_term="AI",
            date_from="2023-01-01",
            queue_url="https://sqs-url",
            logger=mock_logger,
        )
