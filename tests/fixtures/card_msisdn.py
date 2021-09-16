import allure
import pytest
from models.database.sequencies import simcard_number_id_seq
from lib.utils import Fake


fake = Fake()


@pytest.fixture
def nonexistent_card_msisdn(clients):
    return clients.DB.card_msisdn.session.execute(simcard_number_id_seq)


@pytest.yield_fixture(scope="class")
def card_msisdn_generator(clients):
    _id = []

    def _get(_, card_id, card_msisdn, card_rate_id, virtual_group_id):
        new_sim_card_msisdn = clients.DB.card_msisdn.create(card_id, card_msisdn, card_rate_id, virtual_group_id)
        _id.append(new_sim_card_msisdn.id)
        return new_sim_card_msisdn

    yield _get

    for i in _id:
        clients.DB.card_series.delete(i)


@pytest.yield_fixture()
def delete_card_msisdn_from_db(clients):
    id = []

    def _get_id(_id):
        _id = int(_id)
        id.append(_id)
        return _id

    yield _get_id

    with allure.step('Delete created base cards from db'):
        for i in id:
            clients.DB.card_msisdn.delete(i)
