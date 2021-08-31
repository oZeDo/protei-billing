import allure
import pytest
from models.database.sequencies import currency_id_seq
from lib.utils import Fake


fake = Fake()


@pytest.fixture
def nonexistent_currency(clients):
    return clients.DB.currency.session.execute(currency_id_seq)


@pytest.yield_fixture(scope="class")
def currency_generator(clients):
    _id = []

    def _get(*args):
        new_currency = clients.DB.currency.create()
        _id.append(new_currency.id)
        return new_currency

    yield _get

    for i in _id:
        clients.DB.currency.delete(i)


@pytest.yield_fixture()
def delete_currency_from_db(clients):
    id = []

    def _get_id(_id):
        _id = int(_id)
        id.append(_id)
        return _id

    yield _get_id

    with allure.step('Delete created currency from db'):
        for i in id:
            clients.DB.currency.delete(i)
