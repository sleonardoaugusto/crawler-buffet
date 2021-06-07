from lxml.html import HtmlElement

from core.stock import Stock


class Parser:
    SYMBOL_XPATH = 'td[@aria-label="Symbol"]/a/text()'
    NAME_XPATH = 'td[@aria-label="Name"]/text()'
    PRICE_XPATH = 'td[@aria-label="Price (Intraday)"]/span/text()'

    def parse(self, stock_elements):
        page_stocks = {}
        for stock_element in stock_elements:
            stock = Stock(
                symbol=self.extract_symbol(stock_element),
                name=self.extract_name(stock_element),
                price=self.extract_price(stock_element),
            )
            page_stocks.update({stock.symbol: stock.serialize()})
        return page_stocks

    def extract_symbol(self, element: HtmlElement):
        return element.xpath(self.SYMBOL_XPATH)[0]

    def extract_name(self, element: HtmlElement):
        try:
            element.xpath(self.NAME_XPATH)[0]
        except IndexError:
            return None

    def extract_price(self, element: HtmlElement):
        return element.xpath(self.PRICE_XPATH)[0]
