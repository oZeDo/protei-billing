import functools
import logging

import allure
import pytest

from lib.utils import Fake
from API.client.rpc import RPCClient
from API.client.db import DBClient


pytest_plugins = [
    "tests.fixtures.cardgroup",
    "tests.fixtures.client",
]

fake = Fake()


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


# @pytest.fixture(scope="class")
# def clients(request):
#     request.cls.DBClient = DBClient()
#     request.cls.RPCClient = RPCClient()
#     return request.cls


@pytest.fixture(autouse=True, scope="class")
def setup_fixture(request, client_generator, cardgroup_generator):
    request.cls.default_client = client_generator()
    request.cls.client_generator = client_generator
    request.cls.cardgroup_generator = cardgroup_generator
    request.cls.default_cardgroup = cardgroup_generator(request.cls.default_client.id)


class Clients:
    RPC = RPCClient()
    DB = DBClient(url='oracle+cx_oracle://pbill:sql@192.168.73.3:1521/orcl')


@pytest.fixture(scope="class", autouse=True)
def clients():
    yield Clients
