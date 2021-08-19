from models.database.reflected_db import Company, Company2role, Companyrole
from models.database.sequencies import company_id_seq, company2role_id_seq
from API.controller.db.base import BaseDBController
from lib.utils import Fake

fake = Fake()


class CompanyRoleDBController(BaseDBController):
    """
    Контроллер с ролями компании. (Read-only)
    """
    def read(self) -> [Companyrole]:
        company_roles: [Companyrole] = self.session.execute(self.session.query(Companyrole))
        self.session.commit()  # !TODO: костыль
        return company_roles



