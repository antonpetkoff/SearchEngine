import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from sqlalchemy.orm import Session
from connection import Base
from connection import engine
from page import Page
from website import Website


class WebCrawler:

    def __init__(self, domain):
        self.domain = domain
        self.scanned_urls = []

        Base.metadata.create_all(engine)
        self.session = Session(bind=engine)

    def is_outgoing(self, url):
        if self.domain not in url:
            return True

        if url.startswith("https://", 0, 8):
            url = url[8:]
        else:
            url = url[7:]       # http://

        if url.startswith("www."):
            url = url[4:]

        if url.startswith(self.domain) and '#' not in url:
            return False

        return True

    def prepare_link(self, url, href):
        return urljoin(url, href)

    def scan_page(self, url):
        if url in self.scanned_urls:
            return

        print(url)
        self.scanned_urls.append(url)

        r = requests.get(url)
        soup = BeautifulSoup(r.text)

        self.save_page_db(url, soup)

        for link in soup.find_all('a'):
            href = link.get('href')
            new_link = self.prepare_link(url, href)
            if not self.is_outgoing(new_link):
                self.scan_page(new_link)

    def scan_website(self, url):
        url = 'http://' + self.domain

        r = requests.get(url)
        soup = BeautifulSoup(r.text)
        self.save_website_db(url, soup)

        self.scan_page(url)

    def save_website_db(self, url, soup):
        args = {
            "url": url,
            "title": "null",        # unhandled
            "domain": self.domain,
            "pages_count": -1,      # unhandled
            "html_ver": "null"      # unhandled
        }
        self.session.add(Website(**args))
        self.session.commit()

    def save_page_db(self, url, soup):
        args = {
            "url": url,
            "title": "null",
            "desc": "null",
            "ads": -1,          # unhandled
            "SSL": False,       # unhandled
            "multilang": -1,    # unhandled
            "points": -1,       # unhandled
            "website_id": 1
        }
        self.session.add(Page(**args))
        self.session.commit()


def main():
    crawler = WebCrawler("syndbg.github.io")
    crawler.scan_website("http://blog.syndbg.com/")


if __name__ == '__main__':
    main()
