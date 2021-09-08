import functools
import logging

import allure
import pytest

from lib.utils import Fake
from API.client.rpc import RPCClient
from API.client.db import DBClient


pytest_plugins = [
    "tests.fixtures.company",
    "tests.fixtures.currency",
    "tests.fixtures.virtual_group",
    "tests.fixtures.account",
    "tests.fixtures.accounting_file",
    "tests.fixtures.card_series",
    "tests.fixtures.base_card",
    "tests.fixtures.card",
    "tests.fixtures.cardgroup",
    "tests.fixtures.client"
]

fake = Fake()


# def safe_teardown(destruction_method):
#     def decorator(func):
#         def wrapper(clients, *args, **kwargs):
#             try:
#                 for i in func(clients, *args, **kwargs):
#                     yield i
#             finally:
#                 destruction_method(clients)
#                 print("я тут был")
#         return wrapper
#     return decorator
#
#
# def cardgroup_destructor(clients):
#     for i in _id:
#         clients.DB.card_group.delete(int(i))


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


class AllureLoggingHandler(logging.Handler):
    def log(self, message):
        with allure.step('Log {}'.format(message)):
            pass

    def emit(self, record):
        self.log("({}) {}".format(record.levelname, record.getMessage()))


class AllureCatchLogs:
    def __init__(self):
        self.rootlogger = logging.getLogger()
        self.allurehandler = AllureLoggingHandler()

    def __enter__(self):
        if self.allurehandler not in self.rootlogger.handlers:
            self.rootlogger.addHandler(self.allurehandler)

    def __exit__(self, exc_type, exc_value, traceback):
        self.rootlogger.removeHandler(self.allurehandler)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_setup():
    with AllureCatchLogs():
        yield


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_call():
    with AllureCatchLogs():
        yield


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_teardown():
    with AllureCatchLogs():
        yield


# @pytest.fixture(autouse=True, scope="class")
# def clients(request):
#     request.cls.DBClient = DBClient("oracle+cx_oracle://pbill:sql@192.168.73.3:1521/orcl")
#     request.cls.RPCClient = RPCClient()
#     return request.cls


@pytest.fixture(autouse=True, scope="class")
def setup_fixture(request, company_generator, currency_generator, virtual_group_generator, account_generator,
                  accounting_file_generator, card_series_generator, base_card_generator, card_generator,
                  client_generator, cardgroup_generator):
    request.cls.company_generator = company_generator
    request.cls.default_company = company_generator()

    request.cls.currency_generator = currency_generator
    request.cls.default_currency = currency_generator()

    request.cls.virtual_group_generator = virtual_group_generator
    request.cls.default_virtual_group = virtual_group_generator(request.cls, request.cls.default_company.id,
                                                                request.cls.default_currency.id)

    request.cls.account_generator = account_generator
    request.cls.default_account = account_generator(request.cls, request.cls.default_currency.id,
                                                    request.cls.default_virtual_group.id)

    request.cls.accounting_file_generator = accounting_file_generator
    request.cls.default_accounting_file = accounting_file_generator(request.cls, request.cls.default_virtual_group.id,
                                                                    request.cls.default_currency.id)

    request.cls.card_series_generator = card_series_generator
    request.cls.default_card_series = card_series_generator(request.cls, request.cls.default_currency.id,
                                                            request.cls.default_accounting_file.id)

    request.cls.base_card_generator = base_card_generator
    request.cls.default_base_card = base_card_generator(request.cls, request.cls.default_virtual_group.id,
                                                        request.cls.default_accounting_file.id)

    request.cls.card_generator = card_generator
    request.cls.default_card = card_generator(request.cls, request.cls.default_account.id,
                                              request.cls.default_base_card.id)

    request.cls.client_generator = client_generator
    request.cls.default_client = client_generator(request.cls, request.cls.default_virtual_group.id)

    request.cls.cardgroup_generator = cardgroup_generator
    request.cls.default_cardgroup = cardgroup_generator(request.cls, request.cls.default_client.id)


class Clients:
    RPC = RPCClient()
    DB = DBClient(url='oracle+cx_oracle://pbill:sql@192.168.73.3:1521/orcl')


@pytest.fixture(scope="class", autouse=True)
def clients():
    yield Clients
