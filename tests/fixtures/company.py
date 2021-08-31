import allure
import pytest
from models.database.sequencies import company_id_seq
from lib.utils import Fake


fake = Fake()


@pytest.fixture
def nonexistent_company(clients):
    return clients.DB.company.session.execute(company_id_seq)


@pytest.yield_fixture(scope="class")
def company_generator(clients):
    _id = []

    def _get(*args):
        new_company = clients.DB.company.create()
        _id.append(new_company.id)
        return new_company

    yield _get

    for i in _id:
        clients.DB.company.delete(i)


@pytest.yield_fixture()
def delete_company_from_db(clients):
    id = []

    def _get_id(_id):
        _id = int(_id)
        id.append(_id)
        return _id

    yield _get_id

    with allure.step('Delete created company from db'):
        for i in id:
            clients.DB.company.delete(i)
