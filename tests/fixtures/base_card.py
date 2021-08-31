import allure
import pytest
from models.database.sequencies import basecard_id_seq
from lib.utils import Fake


fake = Fake()


@pytest.fixture
def nonexistent_base_card(clients):
    return clients.DB.base_card.session.execute(basecard_id_seq)


@pytest.yield_fixture(scope="class")
def base_card_generator(clients):
    _id = []

    def _get(_, virtual_group_id, accounting_file_id, state=2, *args):
        new_base_card = clients.DB.base_card.create(virtual_group_id, accounting_file_id, state)
        _id.append(new_base_card.id)
        return new_base_card

    yield _get

    for i in _id:
        clients.DB.base_card.delete(i)


@pytest.yield_fixture()
def delete_base_card_from_db(clients):
    id = []

    def _get_id(_id):
        _id = int(_id)
        id.append(_id)
        return _id

    yield _get_id

    with allure.step('Delete created base cards from db'):
        for i in id:
            clients.DB.base_card.delete(i)
