import allure
import pytest
from models.database.sequencies import virtual_group_id_seq
from lib.utils import Fake

fake = Fake()


@pytest.fixture
def nonexistent_virtual_group(clients):
    return clients.DB.virtual_group.session.execute(virtual_group_id_seq)


@pytest.yield_fixture(scope="class")
def virtual_group_generator(clients):
    _id = []

    def _get(_, company_id, currency_id, *args):
        # print(a)  # <tests.tests.test_card_group.test_card_group.TestCreation object at 0x000002A2CD420C40>
        print(f"Фикстура\nКомпания:{company_id}, Валюта:{currency_id}, {args}")
        new_virtual_group = clients.DB.virtual_group.create(company_id, currency_id)
        _id.append(new_virtual_group.id)
        return new_virtual_group

    yield _get

    for i in _id:
        clients.DB.virtual_group.delete(i)


@pytest.yield_fixture()
def delete_virtual_group_from_db(clients):
    id = []

    def _get_id(_id):
        _id = int(_id)
        id.append(_id)
        return _id

    yield _get_id

    with allure.step('Delete created virtual group from db'):
        for i in id:
            clients.DB.virtual_group.delete(i)
