import pytest
import requests

from core.crawler import Crawler
from core.parser import Parser

PAGE_1 = 'https://finance.yahoo.com/screener/unsaved/d4688fa1-403b-4850-8598-91cb24a80aad?count=25&offset=0'
PAGE_2 = 'https://finance.yahoo.com/screener/unsaved/d4688fa1-403b-4850-8598-91cb24a80aad?offset=25&count=25'
PAGE_3 = 'https://finance.yahoo.com/screener/unsaved/d4688fa1-403b-4850-8598-91cb24a80aad?count=25&offset=50'


@pytest.fixture
def fix_urls():
    return [PAGE_1, PAGE_2, PAGE_3]


@pytest.fixture
def fix_crawler(fix_urls):
    return Crawler(urls=fix_urls, client=requests, parser=Parser())


def test_init(fix_crawler, fix_urls):
    assert fix_crawler.urls == fix_urls
    assert fix_crawler.client == requests
    assert isinstance(fix_crawler.parser, Parser)


@pytest.mark.vcr
def test_fetch_stocks(fix_crawler):
    assert len(fix_crawler.fetch_stocks()) == 75
