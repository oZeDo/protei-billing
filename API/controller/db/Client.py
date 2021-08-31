from models.database.reflected_db import Client, Virtualgroup
from models.database.sequencies import client_id_seq
from API.controller.db.base import BaseDBController
from lib.utils import Fake

fake = Fake()


class ClientDBController(BaseDBController):

    def create(self, virtualgroup_id) -> Client:
        client = Client(id=client_id_seq.next_value(),
                        clienttypeid=1,
                        dname=fake.name(),
                        vgroupid=virtualgroup_id,
                        billmode_id=1)
        self.session.add(client)
        self.session.commit()
        return client

    def delete(self, client_id):
        self.session.query(Client).filter(Client.id == client_id).delete()
        self.session.commit()

    def execute(self, statement, **kwargs):
        return self.session.execute(statement, **kwargs)
