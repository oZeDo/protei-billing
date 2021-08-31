import allure
import pytest
from models.database.sequencies import account_id_seq
from lib.utils import Fake


fake = Fake()


@pytest.fixture
def nonexistent_account(clients):
    return clients.DB.account.session.execute(account_id_seq)


@pytest.yield_fixture(scope="class")
def account_generator(clients):
    _id = []

    def _get(_, currency_id, virtual_group_id, *args):
        new_account = clients.DB.account.create(currency_id, virtual_group_id)
        _id.append(new_account.id)
        return new_account

    yield _get

    for i in _id:
        clients.DB.account.delete(i)


@pytest.yield_fixture()
def delete_account_from_db(clients):
    id = []

    def _get_id(_id):
        _id = int(_id)
        id.append(_id)
        return _id

    yield _get_id

    with allure.step('Delete created accounts from db'):
        for i in id:
            clients.DB.account.delete(i)
