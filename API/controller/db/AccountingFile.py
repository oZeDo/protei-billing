from models.database.reflected_db import Accountingfile, Virtualgroup, Currency
from models.database.sequencies import accounting_file_id_seq
from API.controller.db.base import BaseDBController
from lib.utils import Fake

fake = Fake()


class AccountingFileDBController(BaseDBController):
    def create(self, mvno: Virtualgroup, currency: Currency) -> Accountingfile:
        accounting_file = Accountingfile(id=accounting_file_id_seq.next_value(),
                                         vgroupid=mvno.id,
                                         state=2,
                                         name=fake.catch_phrase(),
                                         currencyid=currency.id,
                                         code=fake.uuid4()[:32])
        self.session.add(accounting_file)
        self.session.commit()
        return accounting_file

    def read(self, accounting_file_id) -> Accountingfile:
        cg_from_db: Accountingfile = self.session.query(Accountingfile).filter(Accountingfile.id == accounting_file_id)\
            .first()
        self.session.commit()  # !TODO: костыль
        return cg_from_db

    def delete(self, accounting_file_id) -> None:
        self.session.query(Accountingfile).filter(Accountingfile.id == accounting_file_id).delete()
        self.session.commit()

