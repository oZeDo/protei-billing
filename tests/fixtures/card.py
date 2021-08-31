import allure
import pytest
from models.database.sequencies import simcard_id_seq
from lib.utils import Fake


fake = Fake()


@pytest.fixture
def nonexistent_card(clients):
    return clients.DB.card.session.execute(simcard_id_seq)


@pytest.yield_fixture(scope="class")
def card_generator(clients):
    _id = []

    def _get(_, account_id, base_card_id, *args):
        new_card = clients.DB.card.create(account_id, base_card_id)
        _id.append(new_card.id)
        return new_card

    yield _get

    for i in _id:
        clients.DB.card_group.delete(i)


@pytest.yield_fixture()
def delete_card_from_db(clients):
    id = []

    def _get_id(_id):
        _id = int(_id)
        id.append(_id)
        return _id

    yield _get_id

    with allure.step('Delete created cards from db'):
        for i in id:
            clients.DB.card.delete(i)
