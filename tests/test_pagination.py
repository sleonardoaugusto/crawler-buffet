import pytest
import requests

from core.crawler import Pagination

BASE_URL = 'https://finance.yahoo.com/screener/unsaved/1f51e753-06ab-47b2-8fc2-6cb511e305c4?dependentField=sector&dependentValues='


@pytest.fixture
def fix_pagination():
    return Pagination(url=BASE_URL, client=requests)


@pytest.mark.vcr
def test_pagination(fix_pagination):
    expect = [
        'https://finance.yahoo.com/screener/unsaved/1f51e753-06ab-47b2-8fc2-6cb511e305c4?dependentField=sector&dependentValues=&offset=0&count=100',
        'https://finance.yahoo.com/screener/unsaved/1f51e753-06ab-47b2-8fc2-6cb511e305c4?dependentField=sector&dependentValues=&offset=100&count=100',
        'https://finance.yahoo.com/screener/unsaved/1f51e753-06ab-47b2-8fc2-6cb511e305c4?dependentField=sector&dependentValues=&offset=200&count=100',
        'https://finance.yahoo.com/screener/unsaved/1f51e753-06ab-47b2-8fc2-6cb511e305c4?dependentField=sector&dependentValues=&offset=300&count=100',
        'https://finance.yahoo.com/screener/unsaved/1f51e753-06ab-47b2-8fc2-6cb511e305c4?dependentField=sector&dependentValues=&offset=400&count=100',
    ]
    assert fix_pagination() == expect
