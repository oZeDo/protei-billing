from models.database.reflected_db import Virtualgroup
from models.database.reflected_db import Simcard, Basecard
from models.database.sequencies import virtual_group_id_seq
from API.controller.db.base import BaseDBController
from lib.utils import Fake

fake = Fake()


class VirtualGroupDBController(BaseDBController):
    def create(self, company_id, currency_id) -> Virtualgroup:
        virtual_group = Virtualgroup(id=virtual_group_id_seq.next_value(),
                                     groupname=fake.company(),
                                     ownercompany=company_id,
                                     defcurrencyid=currency_id)
        self.session.add(virtual_group)
        self.session.commit()
        return virtual_group

    def read(self, virtual_group_id) -> Virtualgroup:
        cg_from_db: Virtualgroup = self.session.query(Virtualgroup).filter(Virtualgroup.id == virtual_group_id).first()
        self.session.commit()  # !TODO: костыль
        return cg_from_db

    def delete(self, virtual_group_id) -> None:
        self.session.query(Virtualgroup).filter(Virtualgroup.id == virtual_group_id).delete()
        self.session.commit()
