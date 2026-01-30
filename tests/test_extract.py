import unittest
from unittest.mock import patch, MagicMock
import requests
from utils.extract import get_html_content, parse_product_card, scrape_all_pages
from bs4 import BeautifulSoup

class TestExtract(unittest.TestCase):

    @patch('utils.extract.requests.get')
    def test_get_html_content_success(self, mock_get):
        # Mock successful response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html>Success</html>"
        mock_get.return_value = mock_response

        result = get_html_content("http://test.com")
        self.assertEqual(result, "<html>Success</html>")

    @patch('utils.extract.requests.get')
    def test_get_html_content_failure(self, mock_get):
        mock_get.side_effect = requests.exceptions.RequestException("Connection Error")
        
        result = get_html_content("http://test.com")
        self.assertIsNone(result)

    def test_parse_product_card_valid(self):
        html = """
        <div class="collection-card">
            <h3 class="product-title">Test Product</h3>
            <span class="price">$100.00</span>
            <div class="product-details">
                <p>Rating: 4.5 / 5</p>
                <p>3 Colors</p>
                <p>Size: M</p>
                <p>Gender: Men</p>
            </div>
        </div>
        """
        soup = BeautifulSoup(html, "html.parser")
        card = soup.find("div")
        
        result = parse_product_card(card)
        self.assertEqual(result['Title'], "Test Product")
        self.assertEqual(result['Price'], "$100.00")
        self.assertIsNotNone(result['Timestamp'])

    @patch('utils.extract.get_html_content')
    def test_scrape_all_pages(self, mock_get_html):
        mock_get_html.return_value = """
        <div class="collection-card">
            <h3 class="product-title">Test Product</h3>
            <span class="price">$50.00</span>
            <div class="product-details"></div>
        </div>
        """
        
        results = scrape_all_pages(start_page=1, end_page=1)
        self.assertTrue(len(results) > 0)
        self.assertEqual(results[0]['Title'], "Test Product")

if __name__ == '__main__':
    unittest.main()
