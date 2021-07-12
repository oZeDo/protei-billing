import pytest

from models.database.sequencies import client_id_seq


@pytest.yield_fixture(scope="class")
def client_generator(db_session, dbapi_fixture):
    _id = []

    def _get(*args):
        new_client = dbapi_fixture.clientDB.create()
        _id.append(new_client.id)
        return new_client

    yield _get

    for i in _id:
        dbapi_fixture.clientDB.delete(i)


@pytest.fixture
def nonexistent_client(db_session):
    return db_session.execute(client_id_seq)

