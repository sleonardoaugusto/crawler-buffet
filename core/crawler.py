import re
from pathlib import Path

from lxml import html
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class Driver:
    BASE_DIR = Path(__file__).resolve().parent.parent
    DRIVER_PATH = 'webdrivers/chromedriver'

    def __init__(self):
        self.driver = Path.joinpath(self.BASE_DIR, self.DRIVER_PATH)

    def get(self, url) -> WebDriver:
        driver = webdriver.Chrome(self.driver)
        driver.get(url)
        return driver


class Pagination:
    STOCKS_PER_PAGE = 100

    def __init__(self, url, client):
        self.url = url
        self.client = client

    def __call__(self, *args, **kwargs):
        total_stocks = self.get_total_stocks()
        return [
            self.build_url(offset)
            for offset in range(0, total_stocks, self.STOCKS_PER_PAGE)
        ]

    def build_url(self, offset):
        return f'{self.url}&offset={offset}&count={self.STOCKS_PER_PAGE}'

    def get_total_stocks(self):
        page = self.client.get(self.url)
        html_tree = html.fromstring(page.content)
        txt = html_tree.xpath(
            '//*[@id="fin-scr-res-table"]/div[1]/div[1]/span[2]/span/text()'
        )[0]
        return int(re.search(r'of (.*?) results', txt).group(1))


class Crawler:
    def __init__(self, urls, client, parser):
        self.urls = urls
        self.client = client
        self.parser = parser

    def fetch_stocks(self):
        stocks = {}

        for url in self.urls:
            stock_elements = self.get_stock_elements(self.client.get(url))
            stocks.update(self.parser.parse(stock_elements))

        return stocks

    def get_stock_elements(self, page):
        html_tree = html.fromstring(page.content)
        stocks_elements = html_tree.xpath(
            '//div[@id="scr-res-table"]/div[1]/table/tbody//tr'
        )
        return stocks_elements


class Filter:
    FIND_STOCKS_BTN_XPATH = (
        '//*[@id="screener-criteria"]/div[2]/div[1]/div[3]/button[1]'
    )
    REGION_FILTER_OPTION_XPATH = '//li/label/span[text()="{region}"]'

    def __init__(self, webdriver):
        self.webdriver = webdriver
        self.clear_region_filters()

    def clear_region_filters(self):
        region_filters = self.webdriver.find_elements_by_class_name('filterItem')
        for region_filter in region_filters:
            region_filter.click()

    def filter_by_region(self, region):
        filter_add_btn = self.webdriver.find_element_by_class_name('filterAdd')
        filter_add_btn.click()
        filter_menu = self.webdriver.find_element_by_id('dropdown-menu')
        region_elem = filter_menu.find_element_by_xpath(
            self.REGION_FILTER_OPTION_XPATH.format(region=region)
        )
        region_elem.click()
        return self.apply_filter()

    def apply_filter(self):
        find_stocks_btn = WebDriverWait(self.webdriver, 30).until(
            EC.element_to_be_clickable((By.XPATH, self.FIND_STOCKS_BTN_XPATH))
        )
        find_stocks_btn.click()
        curr_url = self.webdriver.current_url
        WebDriverWait(self.webdriver, 30).until(
            lambda driver: driver.current_url != curr_url
        )
        return self.webdriver.current_url
