from unittest.mock import patch, MagicMock
from guardian_api import fetch_guardian_articles, get_api_key

# import pytest


class TestGuardianAPI:

    @patch("guardian_api.requests.get")
    def test_fetch_guardian_articles_success(self, mock_requests_get):
        # Sample api key
        dummy_api_key = "test-api-key"
        logger = MagicMock()

        # Mock the response
        mock_response = {
            "response": {
                "results": [
                    {
                        "webPublicationDate": "2023-01-01T10:00:00Z",
                        "webTitle": "Sample Title",
                        "webUrl": "https://example.com/article",
                        "fields": {
                            "bodyText": "This is a sample for testing."
                        },
                    }
                ]
            }
        }

        mock_requests_get.return_value.status_code = 200
        mock_requests_get.return_value.json.return_value = mock_response

        articles = fetch_guardian_articles(
            guardian_api_key=dummy_api_key, search_term="test", logger=logger
        )

        # Asserting returned article
        # matches with mock one
        assert len(articles) == 1
        article = articles[0]
        assert article["webTitle"] == "Sample Title"
        assert article["content_preview"].startswith("This is a sample")

        # Checking logger
        logger.info.assert_any_call("Calling api...")
        logger.info.assert_any_call("Returning formatted data...")

    def test_fetch_guardian_articles_api_key_empty(self):
        # None api key
        invalid_api_key = None
        mock_logger = MagicMock()

        articles = fetch_guardian_articles(
            guardian_api_key=invalid_api_key,
            search_term="",
            date_from="",
            logger=mock_logger,
        )
        # Validating return value of empty list
        assert articles == []

        mock_logger.error.assert_any_call(
            f"Guardian api key empty: {invalid_api_key}"
        )

        # Empty api key
        invalid_api_key = ""
        articles = fetch_guardian_articles(
            guardian_api_key=invalid_api_key,
            search_term="",
            date_from="",
            logger=mock_logger,
        )
        # Validating return value of empty list
        assert articles == []
        mock_logger.error.assert_any_call(
            f"Guardian api key empty: {invalid_api_key}"
        )

    @patch("guardian_api.requests.get")
    def test_fetch_guardian_articles_invalid_api_key(self, mock_requests_get):
        # Invalid api key
        invalid_api_key = "invalid-api-key"
        # Get raises an error of 403
        status_code = 403
        mock_logger = MagicMock()

        mock_requests_get.return_value.status_code = status_code
        mock_requests_get.return_value.json.return_value = {
            "response": {"results": []}
        }
        fetch_guardian_articles(
            guardian_api_key=invalid_api_key,
            search_term="machine learning",
            date_from="2025-01-01",
            logger=mock_logger,
        )

        mock_logger.error.assert_called_with(
            f"Received response - status code: {403}"
        )

    # @pytest.mark.skip
    @patch("guardian_api.boto3.client")
    def test_get_api_key_success(self, mock_boto_client):

        mock_secret_value = "mock-secret-value"
        # Mocking the logger
        logger = MagicMock()

        mock_secrets_client = MagicMock()
        mock_boto_client.return_value = mock_secrets_client
        mock_secrets_client.get_secret_value.return_value = {
            # Sample secret api key
            "SecretString": mock_secret_value
        }

        # Retrieving secret key and making sure it matches
        secret = get_api_key(secret_name="guardian_api_key", logger=logger)
        assert secret == mock_secret_value
        logger.info.assert_any_call(
            "Calling secrets manager for API Key -> guardian_api_key..."
        )
        logger.info.assert_any_call("Found API Key")

    @patch("guardian_api.boto3.client")
    def test_get_api_key_invalid_secret_name(self, mock_boto_client):
        mock_logger = MagicMock()

        # Mocking secrets client that raises an error
        mock_client = MagicMock()
        mock_boto_client.return_value = mock_client
        mock_client.get_secret_value.side_effect = Exception(
            "Secret not found"
        )

        secret = get_api_key(secret_name="fake_name", logger=mock_logger)

        assert secret is None
        mock_logger.error.assert_called_with(
            "Failed to retrieve secret: Secret not found"
        )
