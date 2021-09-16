import allure
import pytest
from models.database.sequencies import simcard_imsi_id_seq
from lib.utils import Fake


fake = Fake()


@pytest.fixture
def nonexistent_card_imsi(clients):
    return clients.DB.card_imsi.session.execute(simcard_imsi_id_seq)


@pytest.yield_fixture(scope="class")
def card_imsi_generator(clients):
    _id = []

    def _get(_, card_id, card_imsi, virtual_group_id):
        new_sim_card_imsi = clients.DB.card_imsi.create(card_id, card_imsi, virtual_group_id)
        _id.append(new_sim_card_imsi.id)
        return new_sim_card_imsi

    yield _get

    for i in _id:
        clients.DB.card_series.delete(i)


@pytest.yield_fixture()
def delete_card_imsi_from_db(clients):
    id = []

    def _get_id(_id):
        _id = int(_id)
        id.append(_id)
        return _id

    yield _get_id

    with allure.step('Delete created base cards from db'):
        for i in id:
            clients.DB.card_imsi.delete(i)
