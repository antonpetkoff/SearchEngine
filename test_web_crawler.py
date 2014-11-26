import unittest
from web_crawler import WebCrawler


class WebCrawlerTests(unittest.TestCase):

    def setUp(self):
        self.crawler = WebCrawler("hackbulgaria.com")

    def test_prepare_link(self):
        url = "http://hackbulgaria.com/"
        href = "/courses/"
        self.assertEqual(self.crawler.prepare_link(url, href),
                         "http://hackbulgaria.com/courses/")

    def test_is_outgoing_false(self):
        self.assertTrue(self.crawler.is_outgoing("http://facebook.com"))

    def test_is_outgoing_true(self):
        url = "https://hackbulgaria.com/media/content_media/"
        url += "JavaScript-Frontend-conspect.pdf"
        self.assertFalse(self.crawler.is_outgoing(url))


if __name__ == '__main__':
    unittest.main()
