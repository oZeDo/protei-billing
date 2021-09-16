from models.database.reflected_db import Simnumber
from models.database.sequencies import simcard_number_id_seq
from API.controller.db.base import BaseDBController
from lib.utils import Fake

fake = Fake()


class SimCardMsisdnDBController(BaseDBController):

    def create(self, card_id, card_msisdn, card_rate_id, virtual_group_id):
        new_sim_card_number = Simnumber(id=simcard_number_id_seq.next_value(),
                                        pnumber=card_msisdn,
                                        simcardid=card_id,
                                        numbertype=1,
                                        norder=1,  # Еще может быть 0
                                        rate_id=card_rate_id,
                                        vgroup_id=virtual_group_id,
                                        operstate=2,
                                        )
        self.session.add(new_sim_card_number)
        self.session.commit()
        return new_sim_card_number

    def read(self, sim_card_number_id):
        cg_from_db: Simnumber = self.session.query(Simnumber).filter(Simnumber.id == sim_card_number_id).first()
        return cg_from_db

    def delete(self, sim_card_number_id):
        self.session.query(Simnumber).filter(Simnumber.id == sim_card_number_id).delete()
        self.session.commit()
