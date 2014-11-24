import requests
from bs4 import BeautifulSoup


class WebCrawler:

    def __init__(self):
        self.scanned_urls = []

    def scan_page(self, url):
        r = requests.get(url)
        soup = BeautifulSoup(r.text)

        for link in soup.find_all('a'):
            href = link.get('href')
            if href not in self.scanned_urls:
                if href.startswith("http", 0, 4):
                    self.scanned_urls.append(href)
                    print(href)
                else:
                    self.scanned_urls.append(url + href)
                    print(url + href)


def main():
    crawler = WebCrawler()
    crawler.scan_page("http://hackbulgaria.com")


if __name__ == '__main__':
    main()
