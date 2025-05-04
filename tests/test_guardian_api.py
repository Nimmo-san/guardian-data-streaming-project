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

    # @pytest.mark.skip
    @patch("guardian_api.boto3.client")
    def test_get_api_key_success(self, mock_boto_client):

        # Mocking the logger
        logger = MagicMock()

        mock_secrets_client = MagicMock()
        mock_boto_client.return_value = mock_secrets_client
        mock_secrets_client.get_secret_value.return_value = {
            # Sample secret api key
            "SecretString": "mock-secret-value"
        }

        # Retrieving secret key and making sure it matches
        secret = get_api_key(secret_name="guardian_api_key", logger=logger)
        assert secret == "mock-secret-value"
