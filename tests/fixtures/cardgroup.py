import functools
import allure
import pytest
from models.database.sequencies import cardgroup_id_seq
from lib.utils import Fake

fake = Fake()


@pytest.fixture
def nonexistent_cardgroup(clients):
    return clients.DB.card_group.session.execute(cardgroup_id_seq)


def safe_teardown(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as E:
            raise E

    return wrapper


def for_all_methods(decorator):
    @functools.wraps(decorator)
    def decorate(cls):
        for attr in cls.__dict__:  # there's propably a better way to do this
            if callable(getattr(cls, attr)):
                setattr(cls, attr, decorator(getattr(cls, attr)))
        return cls

    return decorate


@pytest.yield_fixture(scope="class")
def cardgroup_generator(clients):
    _id = []

    def _get(client_id, *args):
        new_cardgroup = clients.DB.card_group.create(client_id)
        _id.append(new_cardgroup.id)
        return new_cardgroup

    yield _get

    for i in _id:
        clients.DB.card_group.delete(i)


@pytest.yield_fixture()
def delete_cardgroup_from_db(clients):
    id = []

    def _get_id(_id):
        _id = int(_id)
        id.append(_id)
        return _id

    yield _get_id

    with allure.step('Delete created card groups from db'):
        for i in id:
            clients.DB.card_group.delete(i)
