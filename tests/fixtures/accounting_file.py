import allure
import pytest
from models.database.sequencies import accounting_file_id_seq
from lib.utils import Fake

fake = Fake()


@pytest.fixture
def nonexistent_accounting_file(clients):
    return clients.DB.accounting_file.session.execute(accounting_file_id_seq)


@pytest.yield_fixture(scope="class")
def accounting_file_generator(clients):
    _id = []

    def _get(_, virtual_group_id, currency_id, *args):
        new_accounting_file = clients.DB.accounting_file.create(virtual_group_id, currency_id)
        _id.append(new_accounting_file.id)
        return new_accounting_file

    yield _get

    for i in _id:
        clients.DB.accounting_file.delete(i)


@pytest.yield_fixture()
def delete_accounting_file_from_db(clients):
    id = []

    def _get_id(_id):
        _id = int(_id)
        id.append(_id)
        return _id

    yield _get_id

    with allure.step('Delete created accounting file from db'):
        for i in id:
            clients.DB.accounting_file.delete(i)
