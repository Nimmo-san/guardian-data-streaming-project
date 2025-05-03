from unittest.mock import patch, MagicMock
from src.main import run, lambda_handler


class TestMain:
    @patch("src.main.fetch_guardian_articles")
    @patch("src.main.send_message_to_sqs")
    def test_run_with_articles(self, mock_send, mock_fetch):
        mock_logger = MagicMock()
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
            "test topic", "2023-01-01", logger=mock_logger
        )
        mock_send.assert_called_once()

    @patch("src.main.logger")
    @patch("src.main.run")
    def test_lambda_handler(self, mock_run, mock_logger):
        event = {
            "search_term": "AI",
            "date_from": "2023-01-01",
            "queue_url": "https://sqs-url",
        }

        lambda_handler(event, None)
        # from unittest.mock import ANY
        mock_run.assert_called_once_with(
            "AI", "2023-01-01", "https://sqs-url", mock_logger
        )
