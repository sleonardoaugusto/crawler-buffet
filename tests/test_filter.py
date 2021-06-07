import pytest

from core.crawler import Filter, Driver

BASE_URL = 'https://finance.yahoo.com/screener/new'


@pytest.fixture(scope='module')
def fix_webdriver():
    driver = Driver()
    page = driver.get(BASE_URL)
    yield page
    page.close()


@pytest.fixture
def fix_filter(fix_webdriver):
    return Filter(webdriver=fix_webdriver)


def test_init(fix_filter, fix_webdriver):
    assert fix_filter.webdriver == fix_webdriver


def test_filter_by_region(fix_filter):
    url_without_region = fix_filter.webdriver.current_url
    url_with_region = fix_filter.filter_by_region(region='Argentina')
    assert not url_with_region == url_without_region
