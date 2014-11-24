import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


class WebCrawler:

    def __init__(self):
        self.scanned_urls = []
        self.base_url = ""

    def is_outgoing(self, url):
        if self.base_url in url:
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

        for link in soup.find_all('a'):
            href = link.get('href')
            new_link = self.prepare_link(url, href)
            if not self.is_outgoing(url):
                self.scan_page(new_link)


def main():
    crawler = WebCrawler()
    crawler.base_url = "http://hackbulgaria.com/"
    crawler.scan_page("http://hackbulgaria.com/")


if __name__ == '__main__':
    main()
