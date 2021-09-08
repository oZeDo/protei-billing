from API.controller.db.CardGroup import CardGroupDBController
from API.controller.db.Client import ClientDBController
from API.controller.db.Card import CardDBController
from API.controller.db.Company import CompanyDBController
from API.controller.db.Company2role import Company2roleDBController
from API.controller.db.CompanyRole import CompanyRoleDBController
from API.controller.db.Currency import CurrencyDBController
from API.controller.db.VirtualGroup import VirtualGroupDBController
from API.controller.db.AccountingFile import AccountingFileDBController
from API.controller.db.Account import AccountDBController
from API.controller.db.Basecard import BaseCardDBController
from API.controller.db.CardSeries import CardSeriesDBController


class DBClient:
    def __init__(self, url: str, pool_size: int = 5, max_overflow: int = 5):
        """Database client, which provides access for all db controllers and methods.

        Args:
            url (str): Database connection string (DSN). Example format: {DRIVER}://{USER}:{PASSWORD}@{HOST}:{PORT}/{SID}
            pool_size (int, optional): Number of connections to be maintained. Defaults to 5.
            max_overflow (int, optional): The maximum overflow size of the pool. Defaults to 5.
        """

        self.card_group = CardGroupDBController(url, pool_size, max_overflow)
        self.client = ClientDBController(url, pool_size, max_overflow)
        self.card = CardDBController(url, pool_size, max_overflow)
        self.company = CompanyDBController(url, pool_size, max_overflow)
        self.company2role = Company2roleDBController(url, pool_size, max_overflow)
        self.company_role = CompanyRoleDBController(url, pool_size, max_overflow)
        self.currency = CurrencyDBController(url, pool_size, max_overflow)
        self.virtual_group = VirtualGroupDBController(url, pool_size, max_overflow)
        self.accounting_file = AccountingFileDBController(url, pool_size, max_overflow)
        self.account = AccountDBController(url, pool_size, max_overflow)
        self.base_card = BaseCardDBController(url, pool_size, max_overflow)
        self.card_series = CardSeriesDBController(url, pool_size, max_overflow)
