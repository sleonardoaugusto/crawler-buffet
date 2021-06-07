import pytest

from core.stock import Stock


@pytest.fixture
def fix_stock_attrs():
    return dict(symbol='AMX.BA', name='América Móvil, S.A.B. de C.V.', price=2089.00)


@pytest.fixture
def fix_stock(fix_stock_attrs):
    return Stock(**fix_stock_attrs)


def test_init(fix_stock, fix_stock_attrs):
    assert fix_stock.symbol == fix_stock_attrs['symbol']
    assert fix_stock.name == fix_stock_attrs['name']
    assert fix_stock.price == fix_stock_attrs['price']


def test_serialize(fix_stock):
    expect = {
        'symbol': fix_stock.symbol,
        'name': fix_stock.name,
        'price': fix_stock.price,
    }
    assert fix_stock.serialize() == expect
