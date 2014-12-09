import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from sqlalchemy.orm import Session
from connection import Base
from connection import engine
from page import Page
from website import Website


class WebCrawler:
    PAGE_COUNTER = 0
    CURR_WEBSITE_ID = 0

    def __init__(self, domain):
        self.domain = domain
        self.scanned_urls = []

        Base.metadata.create_all(engine)
        self.session = Session(bind=engine)

    def is_outgoing(self, url):
        if self.domain not in url:
            return True

        if url.startswith('https://', 0, 8):
            url = url[8:]
        else:
            url = url[7:]       # http://

        if url.startswith('www.'):
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

        self.PAGE_COUNTER += 1

        for link in soup.find_all('a'):
            href = link.get('href')
            new_link = self.prepare_link(url, href)
            if not self.is_outgoing(new_link):
                self.scan_page(new_link)

    def scan_website(self, url):
        url = 'http://' + self.domain

        if self.is_domain_crawled(self.domain):
            return

        self.CURR_WEBSITE_ID = 1 + self.get_last_website_id()

        self.scan_page(url)     # crawl pages to get pages_count
        pages_count = self.PAGE_COUNTER
        self.PAGE_COUNTER = 0

        r = requests.get(url)
        soup = BeautifulSoup(r.text)
        self.save_website_db(url, soup, pages_count)

    def save_website_db(self, url, soup, pages_count):
        args = {
            'url': url,
            'title': self.get_page_title(soup),
            'domain': self.domain,
            'pages_count': pages_count,
            'html_5': self.is_html_5(soup)
        }
        self.session.add(Website(**args))
        self.session.commit()

    def save_page_db(self, url, soup):
        args = {
            'url': url,
            'title': self.get_page_title(soup),
            'desc': self.get_page_content(soup),
            'ads': -1,          # unhandled
            'SSL': False,       # unhandled
            'multilang': -1,    # unhandled
            'points': -1,       # unhandled
            'website_id': self.CURR_WEBSITE_ID
        }
        self.session.add(Page(**args))
        self.session.commit()

    def get_last_website_id(self):
        websites = self.session.query(Website).all()
        return len(websites)

    def is_domain_crawled(self, domain):
        result = self.session.query(Website).\
            filter(Website.domain == domain).all()
        return True if len(result) > 0 else False

    def get_page_title(self, soup):
        title = soup.find('meta', {'property': 'og:title'})
        if title is None:
            title = soup.title
            return '' if title is None else title.string
        else:
            return title['content']

    def get_page_content(self, soup):
        desc = soup.find('meta', {'property': 'og:description'})
        if desc is None:
            desc = soup.find('meta', {'name': 'description'})
            return '' if desc is None else desc['content']
        else:
            return desc['content']

    def is_html_5(self, soup):
        html = soup.prettify()
        if html.find('<!DOCTYPE doctype html>') != -1 or \
           html.find('<!DOCTYPE html>') != -1:
            return True
        return False


def main():
    #crawler = WebCrawler('syndbg.github.io')
    #crawler.scan_website('http://blog.syndbg.com/')
    #crawler = WebCrawler('hackbulgaria.com')
    #crawler.scan_website('http://hackbulgaria.com/')
    crawler = WebCrawler('blog.hackbulgaria.com')
    crawler.scan_website('http://blog.hackbulgaria.com/')

    # r = requests.get('http://blog.hackbulgaria.com')
    # soup = BeautifulSoup(r.text)
    # print(crawler.get_page_title(soup))

if __name__ == '__main__':
    main()
