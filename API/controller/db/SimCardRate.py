from models.database.reflected_db import Simnumberrate
from models.database.sequencies import simcard_number_rate_id_seq
from API.controller.db.base import BaseDBController
from lib.utils import Fake

fake = Fake()


class SimCardNumberRateDBController(BaseDBController):

    def create(self, currency_id, virtual_group_id):
        new_sim_card_number_rate = Simnumberrate(id=simcard_number_rate_id_seq.next_value(),
                                            vgroup_id=virtual_group_id,
                                            rate_name=fake.name(),
                                            rate_cost=5,
                                            currency_id=currency_id
                                        )
        self.session.add(new_sim_card_number_rate)
        self.session.commit()
        return new_sim_card_number_rate

    def read(self, sim_card_number_rate_id):
        cg_from_db: Simnumberrate = self.session.query(Simnumberrate).filter(
            Simnumberrate.id == sim_card_number_rate_id).first()
        return cg_from_db

    def delete(self, sim_card_number_rate_id):
        self.session.query(Simnumberrate).filter(Simnumberrate.id == sim_card_number_rate_id).delete()
        self.session.commit()
