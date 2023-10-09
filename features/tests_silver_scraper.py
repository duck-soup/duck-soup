'''
Tests for modules in the silver_scraper package.
'''

import unittest
from silver_scraper import Silver_Scraper

test_url = "https://en.wikipedia.org/wiki/Python_(programming_language)"
class TestSilverScraper(unittest.TestCase):

    def setUp(self):
        # Create an instance of Silver_Scraper with a test URL
        self.scraper = Silver_Scraper(url=test_url)

    def test_get_wiki_text(self):
        # Test the get_wiki_text method with no chapter specified
        text, chapters = self.scraper.get_wiki_text()
        self.assertIsInstance(text, str)
        self.assertIsInstance(chapters, list)

    def test_get_text_from_url(self):
        # Test the get_text_from_url method with no chapter specified
        text, chapters = self.scraper.get_text_from_url()
        self.assertIsInstance(text, str)
        self.assertIsInstance(chapters, list)

# Run the tests
if __name__ == "__main__":
    unittest.main()
