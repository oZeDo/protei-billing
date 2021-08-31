from models.database.reflected_db import Simcard, Account
from models.database.sequencies import simcard_id_seq
from API.controller.db.base import BaseDBController
from lib.utils import Fake

fake = Fake()


class CardDBController(BaseDBController):

    def create(self, account_id, base_card_id):
        new_sim = Simcard(id=simcard_id_seq.next_value(),
                          imsi=fake.uuid4(),
                          account=account_id,
                          iccid=fake.uuid4()[:32],
                          cardid=base_card_id,
                          msisdn=fake.uuid4()[:32]
                          )
        self.session.add(new_sim)
        self.session.commit()
        return new_sim

    def read(self, sim_card_id):
        cg_from_db: Simcard = self.session.query(Simcard).filter(Simcard.id == sim_card_id).first()
        return cg_from_db

    def delete(self, sim_card_id):
        self.session.query(Simcard).filter(Simcard.id == sim_card_id).delete()
        self.session.commit()
