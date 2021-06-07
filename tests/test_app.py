import pytest

from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client


@pytest.fixture
def fix_stock():
    return {'AAPL.BA': {'name': None, 'price': '2,103.50', 'symbol': 'AAPL.BA'}}


@pytest.fixture
def fix_get_stocks(mocker, fix_stock):
    mocker.patch('app.get_stocks', return_value=fix_stock)


def test_stocks(client, fix_get_stocks, fix_stock):
    assert client.get('/stocks/Argentina/').json == fix_stock
