from models.database.reflected_db import Cardgroup
from models.database.sequencies import cardgroup_id_seq
from lib.helpers.db_helpers import commit_changes
from lib.utils import Fake


fake = Fake()


class CardGroupDBAPI(object):
    def __init__(self, db_session):
        self.__db_session = db_session

    @property
    def db_session(self):
        return self.__db_session

    @db_session.setter
    def db_session(self, new_db_session):
        self.__db_session = new_db_session

    def create(self, client_id):
        new_cardgroup = Cardgroup(id=cardgroup_id_seq.next_value(),
                                  cg_name=fake.name(),
                                  cg_info=fake.name(),
                                  client_id=client_id
                                  )
        self.__db_session.add(new_cardgroup)
        commit_changes(self.__db_session)
        return new_cardgroup

    def update(self, data):
        raise NotImplementedError

    def read(self, group_id):

        cg_from_db: Cardgroup = self.__db_session.query(Cardgroup).filter(Cardgroup.id == group_id).first()

        return cg_from_db

    def delete(self, group_id):
        self.__db_session.query(Cardgroup).filter(Cardgroup.id == group_id).delete()
        self.__db_session.commit()
