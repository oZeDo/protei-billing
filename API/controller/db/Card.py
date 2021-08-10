from models.database.reflected_db import Accountingfile, Virtualgroup, Company, Company2role, Companyrole, Currency, \
    Client, Simcard, Account
from models.database.sequencies import virtual_group_id_seq, company_id_seq, company2role_id_seq, currency_id_seq,\
    accounting_file_id_seq, client_id_seq
from API.controller.db.base import BaseDBController
from lib.utils import Fake

fake = Fake()


class CardDBController(BaseDBController):

    def create_company(self) -> Company:
        company = Company(id=company_id_seq.next_value(),
                          comp_name=fake.company(),
                          comp_code=fake.uuid4())
        self.session.add(company)
        self.session.commit_changes()
        return company

    def add_roles_to_company(self, company: Company) -> None:
        company_roles = self.session.execute(self.session.query(Companyrole.id))
        for role in [r for r, in company_roles]:
            self.session.add(Company2role(id=company2role_id_seq.next_value(), companyid=company.id, roleid=role))
        self.session.commit_changes()

    def create_currency(self) -> Currency:
        currency = Currency(id=currency_id_seq.next_value(),
                            name=fake.currency_name(),
                            code="#Q0",
                            baserate=1,
                            precision=2,
                            displayorder=self.session.query(Companyrole.id).count())
        self.session.add(currency)
        self.session.commit_changes()
        return currency

    def create_mnvo(self, company: Company, currency: Currency) -> Virtualgroup:
        virtual_group = Virtualgroup(id=virtual_group_id_seq.next_value(),
                                     groupname=fake.company(),
                                     ownercompany=company.id,
                                     defcurrencyid=currency.id)
        self.session.add(virtual_group)
        self.session.commit_changes()
        return virtual_group

    def create_accounting_file(self, mvno: Virtualgroup, currency: Currency) -> Accountingfile:
        accounting_file = Accountingfile(id=accounting_file_id_seq,
                                         vgroupid=mvno.id,
                                         state=2,
                                         name=fake.catch_phrase(),
                                         currencyid=currency.id,
                                         code=fake.uuid4()[:32])
        self.session.add(accounting_file)
        self.session.commit_changes()
        return accounting_file

    def create_client(self, mvno: Virtualgroup) -> Client:
        client = Client(id=client_id_seq,
                        clienttypeid=1,
                        dname=fake.name(),
                        vgroupid=mvno.id,
                        billmode_id=1)
        self.session.add(client)
        self.session.commit_changes()
        return client

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
