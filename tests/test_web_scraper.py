import pytest
from web_scraping.web_scraper import scrape_data

def test_scrape_data():
    url = "https://example.com"
    result = scrape_data(url)
    assert result is not None
    assert isinstance(result, dict)