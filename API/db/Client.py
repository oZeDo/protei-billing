from models.database.reflected_db import Client
from models.database.sequencies import client_id_seq
from lib.helpers.db_helpers import commit_changes
from lib.utils import Fake


fake = Fake()


class ClientDBAPI:
    def __init__(self, db_session):
        self.__db_session = db_session

    @property
    def db_session(self):
        return self.__db_session

    @db_session.setter
    def db_session(self, new_db_session):
        self.__db_session = new_db_session

    def create(self):
        new_client = Client(id=client_id_seq.next_value(),
                        clienttypeid='2',
                        dname=fake.name(),
                        bank_details='{"inn":"400324093240324","okpo":"3004934","kpp":"40093204934","bankname":"Bank","settlacc":"40090394039409324","corracc":"40049309403294322","bik":"40093","ogrn":null}',
                        vgroupid='1',
                        dname_up=fake.name(),
                        apptype=0,
                        ntf_method='sms',
                        billmode_id='2')

        self.__db_session.add(new_client)
        commit_changes(self.__db_session)

        return new_client

    def update(self, data):
        raise NotImplementedError

    def read(self, group_id):
        raise NotImplementedError

    def delete(self, client_id):
        self.__db_session.query(Client).filter(Client.id == client_id).delete()
        self.__db_session.commit()
