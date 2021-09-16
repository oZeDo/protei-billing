from models.database.reflected_db import Simcardimsi
from models.database.sequencies import simcard_imsi_id_seq
from API.controller.db.base import BaseDBController
from lib.utils import Fake

fake = Fake()


class SimCardImsiDBController(BaseDBController):

    def create(self, card_id, card_imsi, virtual_group_id):
        new_sim_card_imsi = Simcardimsi(id=simcard_imsi_id_seq.next_value(),
                                        imsi=card_imsi,
                                        simcardid=card_id,
                                        state=2,
                                        vgroup_id=virtual_group_id,
                                        )
        self.session.add(new_sim_card_imsi)
        self.session.commit()
        return new_sim_card_imsi

    def read(self, sim_card_imsi_id):
        cg_from_db: Simcardimsi = self.session.query(Simcardimsi).filter(Simcardimsi.id == sim_card_imsi_id).first()
        return cg_from_db

    def delete(self, sim_card_imsi_id):
        self.session.query(Simcardimsi).filter(Simcardimsi.id == sim_card_imsi_id).delete()
        self.session.commit()
