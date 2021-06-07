import pytest
import requests
from lxml import html

from core.parser import Parser


@pytest.fixture
def fix_page():
    page = requests.get(
        'https://finance.yahoo.com/screener/unsaved/bd82dcf6-3c34-41cf-a22d-39362dfa4d97?dependentField=sector&dependentValues='
    )
    return page


@pytest.fixture
def fix_stock_elements(fix_page):
    html_tree = html.fromstring(fix_page.content)
    stocks_elements = html_tree.xpath(
        '//div[@id="scr-res-table"]/div[1]/table/tbody//tr'
    )
    return stocks_elements


@pytest.mark.vcr
def test_parser(fix_stock_elements):
    parser = Parser()
    stocks = parser.parse(fix_stock_elements)
    assert len(stocks) == 25
