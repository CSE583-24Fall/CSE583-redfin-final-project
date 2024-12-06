import unittest
from unittest.mock import patch, MagicMock, mock_open
import requests
import sys
import os

# Add the 'src' directory to sys.path so Python can find the redfinprediction package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from redfinprediction.downloadrawdata import download_and_unzip_file


class TestDownloadRawData(unittest.TestCase):

    @patch("redfinprediction.downloadrawdata.requests.get")
    @patch("builtins.open", new_callable=mock_open)
    @patch("gzip.GzipFile")
    def test_download_and_unzip_file_success(self, mock_gzip, mock_open_file, mock_requests_get):
        # Mock the response object from requests
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.raw = MagicMock()
        mock_requests_get.return_value = mock_response

        # Mock GzipFile context manager to simulate unzipping
        mock_gzip.return_value.__enter__.return_value.read.return_value = b"Sample Data"

        # Call the function
        download_and_unzip_file("https://dummy-url.com", "../../data/raw/city_market_tracker.tsv")

        # Assertions to verify the function behavior
        mock_requests_get.assert_called_once_with("https://dummy-url.com", stream=True)
        mock_gzip.assert_called_once_with(fileobj=mock_response.raw)
        mock_open_file.assert_called_once_with("../../data/raw/city_market_tracker.tsv", "wb")
        mock_open_file().write.assert_called_once_with(b"Sample Data")

    @patch("redfinprediction.downloadrawdata.requests.get")
    def test_download_and_unzip_file_failure_http_error(self, mock_requests_get):
        # Mock a failed HTTP response
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_requests_get.return_value = mock_response

        # Expecting the function to raise an exception due to HTTP failure
        with self.assertRaises(Exception) as context:
            download_and_unzip_file("https://dummy-url.com", "../../data/raw/city_market_tracker.tsv")

        self.assertIn("Download failed", str(context.exception))
        mock_requests_get.assert_called_once_with("https://dummy-url.com", stream=True)

    @patch("redfinprediction.downloadrawdata.requests.get")
    def test_download_and_unzip_file_failure_network_error(self, mock_requests_get):
        # Simulate a network error by raising a requests.ConnectionError
        mock_requests_get.side_effect = requests.ConnectionError("Network error")

        with self.assertRaises(Exception) as context:
            download_and_unzip_file("https://dummy-url.com", "../../data/raw/city_market_tracker.tsv")

        # Assert that the error message matches the simulated network error
        self.assertIn("Network error", str(context.exception))
        mock_requests_get.assert_called_once_with("https://dummy-url.com", stream=True)


if __name__ == "__main__":
    unittest.main()
