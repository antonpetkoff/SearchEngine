import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


class WebCrawler:

    def __init__(self, domain):
        self.domain = domain
        self.scanned_urls = []

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

        for link in soup.find_all('a'):
            href = link.get('href')
            new_link = self.prepare_link(url, href)
            if not self.is_outgoing(new_link):
                self.scan_page(new_link)

    def scan_website(self, url):
        url = 'http://' + self.domain
        self.scan_page(url)


def main():
    crawler = WebCrawler("hackbulgaria.com")
    crawler.scan_website("http://hackbulgaria.com/")


if __name__ == '__main__':
    main()
