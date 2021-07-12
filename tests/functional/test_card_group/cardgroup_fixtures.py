import allure
import pytest


from models.database.sequencies import cardgroup_id_seq
from lib.utils import Fake


fake = Fake()


@pytest.fixture
def nonexistent_cardgroup(db_session):
    return db_session.execute(cardgroup_id_seq)


@pytest.yield_fixture(scope="class")
def cardgroup_generator(dbapi_fixture):
    _id = []
    def _get(client_id, *args):
        new_cardgroup = dbapi_fixture.cardGroupDB.create(client_id)
        _id.append(new_cardgroup.id)
        return new_cardgroup

    yield _get

    for i in _id:
        dbapi_fixture.cardGroupDB.delete(i)


@pytest.yield_fixture()
def delete_cardgroup_from_db(dbapi_fixture):

    id = []

    def _get_id(_id):
        _id = int(_id)
        id.append(_id)
        return _id

    yield _get_id

    with allure.step('Delete created card groups from db'):
        for i in id:
            dbapi_fixture.cardGroupDB.delete(i)
