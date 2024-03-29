from models.database.reflected_db import Cardgroup
from models.database.sequencies import cardgroup_id_seq
from API.controller.db.base import BaseDBController
from lib.utils import Fake

fake = Fake()


class CardGroupDBController(BaseDBController):
    def create(self, client_id) -> Cardgroup:
        new_cardgroup = Cardgroup(id=cardgroup_id_seq.next_value(),
                                  cg_name=fake.name(),
                                  cg_info=fake.name(),
                                  client_id=client_id
                                  )
        self.session.add(new_cardgroup)
        self.session.commit()
        return new_cardgroup

    def read(self, group_id) -> Cardgroup:
        cg_from_db: Cardgroup = self.session.query(Cardgroup).filter(Cardgroup.id == group_id).first()
        self.session.commit()  # !TODO: Спросить про костыль
        return cg_from_db

    def delete(self, group_id) -> None:
        self.session.query(Cardgroup).filter(Cardgroup.id == group_id).delete()
        self.session.commit()
