import requests
from flask import Flask

from core.crawler import Driver, Filter, Pagination, Crawler
from core.parser import Parser

app = Flask(__name__)

STOCKS_URL = 'https://finance.yahoo.com/screener/new'


def get_stocks(region):
    driver = Driver()
    page = driver.get(STOCKS_URL)
    filter = Filter(webdriver=page)
    url = filter.filter_by_region(region)
    page.close()
    pagination = Pagination(url, requests)()
    return Crawler(pagination, requests, Parser()).fetch_stocks()


@app.route('/stocks/<region>/')
def hello_world(region):
    stocks = get_stocks(region=region)
    return stocks


if __name__ == '__main__':
    app.run()
