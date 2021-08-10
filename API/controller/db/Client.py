from models.database.reflected_db import Client
from models.database.sequencies import client_id_seq
from API.controller.db.base import BaseDBController
from lib.utils import Fake

fake = Fake()


class ClientDBController(BaseDBController):

    def create(self):
        new_client = Client(id=client_id_seq.next_value(),
                            clienttypeid='2',
                            dname=fake.name(),
                            bank_details='{"inn":"400324093240324","okpo":"3004934","kpp":"40093204934",'
                                         '"bankname":"Bank","settlacc":"40090394039409324",'
                                         '"corracc":"40049309403294322","bik":"40093","ogrn":null}',
                            vgroupid='1',
                            dname_up=fake.name(),
                            apptype=0,
                            ntf_method='sms',
                            billmode_id='2')
        self.session.add(new_client)
        self.session.commit()
        return new_client

    def delete(self, client_id):
        self.session.query(Client).filter(Client.id == client_id).delete()
        self.session.commit()

    def execute(self, statement, **kwargs):
        return self.session.execute(statement, **kwargs)
