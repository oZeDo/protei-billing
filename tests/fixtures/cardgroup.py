import functools
from functools import wraps

import allure
import pytest


from models.database.sequencies import cardgroup_id_seq
from lib.utils import Fake


fake = Fake()


@pytest.fixture
def nonexistent_cardgroup(clients):
    return clients.DB.card_group.session.execute(cardgroup_id_seq)


#
# class CardGroup:
#     def __init__(self):
#         self._id = []
#
#     @pytest.yield_fixture(scope="class", autouse=True)
#     @safe_teardown
#     def card_group_generator(self, clients):
#         def _get(client_id, *args):
#             new_cardgroup = clients.DB.card_group.create(client_id)
#             self._id.append(new_cardgroup.id)
#             return new_cardgroup
#         yield _get
#
#     @pytest.fixture()
#     def card_group_destructor(self, clients):
#         for i in self._id:
#             clients.DB.card_group.delete(i)

# @pytest.yield_fixture(scope="class")
# def cardgroup_generator(clients):
#     _id = []
#     print("Меня вызволи")
#     def _get(client_id, *args):
#         print("Пим")
#         new_cardgroup = clients.DB.card_group.create(client_id)
#         _id.append(new_cardgroup.id)
#         return new_cardgroup
#     print("пам")
#     yield _get
#     print("Ачистил ->", _id)
#     for i in _id:
#         clients.DB.card_group.delete(i)


# # Первый способ
# @pytest.yield_fixture(scope="class")
# def cardgroup_generator(clients):
#     _id = []
#
#     def _get(client_id, *args):
#         new_cardgroup = clients.DB.card_group.create(client_id)
#         _id.append(new_cardgroup.id)
#         return new_cardgroup
#     try:
#         yield _get
#     finally:
#         for i in _id:
#             clients.DB.card_group.delete(i)
#
#
# # Второй способ
# def safe_teardown(destruction_method):
#     def decorator(func):
#         def wrapper(clients, *args, **kwargs):
#             try:
#                 for i in func(clients, *args, **kwargs):
#                     yield i
#             # except Exception as exception:
#             #     print(exception)
#             #     destruction_method(clients)
#             #     raise exception
#             # finally:
#             #     destruction_method(clients)
#             #     print("я тут был")
#         return wrapper
#     return decorator
#
#
# def cardgroup_destructor(clients):
#     for i in _id:
#         clients.DB.card_group.delete(int(i))
#
#
# @pytest.yield_fixture(scope="class")
# @safe_teardown(destruction_method=cardgroup_destructor)
# def cardgroup_generator(clients):
#     global _id
#     _id = []
#
#     def _get(client_id, *args):
#         new_cardgroup = clients.DB.card_group.create(client_id)
#         _id.append(new_cardgroup.id)
#         return new_cardgroup
#     yield _get


# Третий способ
def safe_teardown(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as E:
            raise E
    return wrapper

# Четвертый способ
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


# Default
# @pytest.yield_fixture(scope="class")
# def cardgroup_generator(clients):
#     _id = []
#     def _get(client_id, *args):
#         new_cardgroup = clients.DB.card_group.create(client_id)
#         _id.append(new_cardgroup.id)
#         return new_cardgroup
#
#     yield _get
#
#     for i in _id:
#         clients.DB.card_group.delete(i)


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
