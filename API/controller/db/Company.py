from models.database.reflected_db import Company, Company2role, Companyrole
from models.database.sequencies import company_id_seq, company2role_id_seq
from API.controller.db.base import BaseDBController
from lib.utils import commit_changes
from lib.utils import Fake

fake = Fake()


class CardDBController(BaseDBController):
    def create(self) -> Company:
        company = Company(id=company_id_seq.next_value(),
                          comp_name=fake.company(),
                          comp_code=fake.uuid4())
        self.session.add(company)
        commit_changes(self.session)
        return company

    def add_roles_to_company(self, company: Company) -> None:
        company_roles = self.session.execute(self.session.query(Companyrole.id))
        for role in [r for r, in company_roles]:
            self.session.add(Company2role(id=company2role_id_seq.next_value(), companyid=company.id, roleid=role))
        commit_changes(self.session)

    def read(self, company_id):
        cg_from_db: Company = self.session.query(Company).filter(Company.id == company_id).first()
        return cg_from_db

    def delete(self, company_id):
        self.session.query(Company).filter(Company.id == company_id).delete()
        self.session.commit()

