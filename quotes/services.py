import time

import requests
from bs4 import BeautifulSoup


class QuotesScraper:
    def __init__(self, url, page_limit):
        self.url = url
        self.page_limit = page_limit
        self.current_page = 0
        self.default_timeout = 3

    def scrap_paginated(self):
        while self.current_page <= self.page_limit:
            self.current_page += 1
            url = self.url + f'{self.current_page}/'
            data = []
            for author, quote, tags in self.scrap(url):
                data.append((author, quote, tags))
            yield data
            time.sleep(self.default_timeout)

    def scrap(self, url):
        response = requests.get(url, headers={
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'
                          ' AppleWebKit/537.36 (KHTML, like Gecko)'
                          ' Chrome/99.0.4844.74 Safari/537.36'})
        response_html = response.text
        soup = BeautifulSoup(response_html, "html.parser")
        content = soup.find_all('div', 'quotes')
        for item in content:
            quote = item.find('span', 'text').text
            author = item.find('small', 'author').text
            tags = item.find('div', 'tags', 'a').text
            yield author, quote, tags
