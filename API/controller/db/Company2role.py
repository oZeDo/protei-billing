from models.database.reflected_db import Company, Company2role, Companyrole
from models.database.sequencies import company_id_seq, company2role_id_seq
from API.controller.db.base import BaseDBController
from lib.utils import Fake

fake = Fake()


class Company2roleDBController(BaseDBController):
    """Контроллер many(Company) to many(CompanyRole)"""
    def create(self, company: Company, role) -> None:
        company_role = Company2role(company2role_id_seq.next_value(),
                                    company=company.id, roleid=role)
        self.session.add(company)
        self.session.commit()

    def read(self, company: Company) -> [Company2role]:
        company_roles: [Company2role] = self.session.query(Company2role).filter(Company2role.company == company.id)
        self.session.commit()  # !TODO: костыль
        return company_roles

    def delete(self, company_id) -> None:
        self.session.query(Company).filter(Company.id == company_id).delete()
        self.session.commit()

