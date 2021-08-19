from models.database.reflected_db import Accountingfile, Virtualgroup, Company, Company2role, Companyrole, Currency, \
    Client, Simcard, Account
from models.database.sequencies import virtual_group_id_seq, company_id_seq, company2role_id_seq, currency_id_seq,\
    accounting_file_id_seq, client_id_seq
from API.controller.db.base import BaseDBController
from lib.utils import Fake

fake = Fake()


class CardDBController(BaseDBController):

    def create(self, client_id):
        new_sim = Simcard()
        self.session.add(new_sim)
        self.session.commit_changes()
        return new_sim

    def read(self, simcard_id):
        cg_from_db: Simcard = self.session.query(Simcard).filter(Simcard.id == simcard_id).first()
        return cg_from_db

    def delete(self, simcard_id):
        self.session.query(Simcard).filter(Simcard.id == simcard_id).delete()
        self.session.commit()
