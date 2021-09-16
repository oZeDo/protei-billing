import allure
import pytest
from models.database.sequencies import card_series_id_seq
from lib.utils import Fake


fake = Fake()


@pytest.fixture
def nonexistent_base_card(clients):
    return clients.DB.card_series.session.execute(card_series_id_seq)


@pytest.yield_fixture(scope="class")
def card_series_generator(clients):
    _id = []

    def _get(_, currency_id, accounting_file_id, amount=5, *args):
        new_card_series = clients.DB.card_series.create(currency_id, accounting_file_id, amount)
        _id.append(new_card_series.id)
        return new_card_series

    yield _get

    for i in _id:
        clients.DB.card_series.delete(i)


@pytest.yield_fixture()
def delete_card_series_from_db(clients):
    id = []

    def _get_id(_id):
        _id = int(_id)
        id.append(_id)
        return _id

    yield _get_id

    with allure.step('Delete created base cards from db'):
        for i in id:
            clients.DB.card_series.delete(i)
