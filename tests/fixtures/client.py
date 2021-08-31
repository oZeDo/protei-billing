import pytest

from models.database.sequencies import client_id_seq


@pytest.yield_fixture(scope="class")
def client_generator(clients):
    _id = []

    def _get(_, virtual_group_id, *args):
        new_client = clients.DB.client.create(virtual_group_id)
        _id.append(new_client.id)
        return new_client

    yield _get

    for i in _id:
        clients.DB.client.delete(i)


@pytest.fixture
def nonexistent_client(clients):
    return clients.DB.client.execute(client_id_seq)
