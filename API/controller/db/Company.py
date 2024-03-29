from models.database.reflected_db import Company, Company2role, Companyrole
from models.database.sequencies import company_id_seq, company2role_id_seq
from API.controller.db.base import BaseDBController
from lib.utils import Fake

fake = Fake()


class CompanyDBController(BaseDBController):
    """Контроллер компании"""
    def create(self) -> Company:
        company = Company(id=company_id_seq.next_value(),
                          comp_name=fake.company(),
                          comp_code=fake.uuid4())
        self.session.add(company)
        self.session.commit()
        return company

    def read(self, company_id) -> Company:
        cg_from_db: Company = self.session.query(Company).filter(Company.id == company_id).first()
        self.session.commit()  # !TODO: костыль
        return cg_from_db

    def delete(self, company_id) -> None:
        self.session.query(Company).filter(Company.id == company_id).delete()
        self.session.commit()
