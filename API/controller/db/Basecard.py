from models.database.reflected_db import Basecard
from models.database.sequencies import basecard_id_seq
from API.controller.db.base import BaseDBController
from lib.utils import Fake

fake = Fake()


class BaseCardDBController(BaseDBController):

    def create(self, virtual_group_id, accounting_file_id, state):
        new_base_card = Basecard(id=basecard_id_seq.next_value(),
                                 cardtype=1,
                                 vgroupid=virtual_group_id,
                                 accfileid=accounting_file_id,
                                 state=state,
                                 cardnumber=fake.uuid4())
        self.session.add(new_base_card)
        self.session.commit()
        return new_base_card

    def read(self, base_card_id):
        cg_from_db: Basecard = self.session.query(Basecard).filter(Basecard.id == base_card_id).first()
        return cg_from_db

    def delete(self, base_card_id):
        self.session.query(Basecard).filter(Basecard.id == base_card_id).delete()
        self.session.commit()
