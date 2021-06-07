import requests
from flask import Flask
from flask_caching import Cache

from core.crawler import Driver, Filter, Pagination, Crawler
from core.parser import Parser

cache = Cache(config={'CACHE_TYPE': 'SimpleCache', 'CACHE_DEFAULT_TIMEOUT': 193})

app = Flask(__name__)
cache.init_app(app)

STOCKS_URL = 'https://finance.yahoo.com/screener/new'


class Stocks:
    BASE_URL = 'https://finance.yahoo.com/screener/new'

    def __init__(self, page):
        self.page = page
        self.filter = Filter(webdriver=page)
        self.pagination = Pagination

    def by_region(self, region):
        url = self.filter.filter_by_region(region)
        return self.get_stock_pages(url)

    def get_stock_pages(self, url):
        stock_urls = Pagination(url, requests)()
        self.page.close()
        return stock_urls


def stocks_factory():
    driver = Driver()
    page = driver.get(STOCKS_URL)
    return Stocks(page)


def get_stocks(region):
    stocks = stocks_factory()
    stock_pages = stocks.by_region(region)
    return Crawler(stock_pages, requests, Parser()).fetch_stocks()


@app.route('/stocks/<region>/')
@cache.cached()
def hello_world(region):
    stocks = get_stocks(region=region)
    return stocks


if __name__ == '__main__':
    app.run()
