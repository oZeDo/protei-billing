import logging

import allure
import pytest


from lib.db_connection import DBConnection
from config.db_consts import DB_ORACLE_HOST, DB_ORACLE_PORT, DB_ORACLE_SID, DB_ORACLE_USERNAME, DB_ORACLE_PASSWORD
from lib.utils import Fake
from API.rpc.CardGroup import CardGroupAPI
from API.db.CardGroup import CardGroupDBAPI
from API.db.Client import ClientDBAPI


pytest_plugins = [
    "tests.functional.test_card_group.cardgroup_fixtures",
    "tests.functional.test_card_group.client_fixtures",
]

fake = Fake()


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


@pytest.fixture(scope="class")
def db_session():
    db_conn = DBConnection(DB_ORACLE_HOST, DB_ORACLE_PORT,
                           DB_ORACLE_SID, DB_ORACLE_USERNAME,
                           DB_ORACLE_PASSWORD)

    yield db_conn.session

    db_conn.close()


@pytest.fixture(autouse=True, scope="class")
def setup_fixture(request, db_session, client_generator, cardgroup_generator, dbapi_fixture, api_fixture):
    request.cls.db_session = db_session
    request.cls.default_client = client_generator()
    request.cls.client_generator = client_generator
    request.cls.cardgroup_generator = cardgroup_generator
    request.cls.default_cardgroup = cardgroup_generator(request.cls.default_client.id)
    request.cls.DBAPI = dbapi_fixture
    request.cls.API = api_fixture


@pytest.fixture(scope="class")
def api_fixture(request):
    request.cls.cardGroupAPI = CardGroupAPI()
    return request.cls


@pytest.fixture(scope="class")
def dbapi_fixture(request, db_session):
    request.cls.cardGroupDB = CardGroupDBAPI(db_session)
    request.cls.clientDB = ClientDBAPI(db_session)
    return request.cls
