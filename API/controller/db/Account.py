from models.database.reflected_db import Account
from models.database.sequencies import account_id_seq
from API.controller.db.base import BaseDBController
from lib.utils import Fake


fake = Fake()


class AccountDBController(BaseDBController):
    def create(self, currency_id, virtual_group_id) -> Account:
        account = Account(id=account_id_seq.next_value(),
                          acctype=1,
                          balance=10 ** 6,
                          limit=0,
                          currency=currency_id,
                          vgroupid=virtual_group_id,
                          state_id=2,  # maybe 1? 0?
                          billing_mode=1  # could be 2 hmm....
                          )
        self.session.add(account)
        self.session.commit()
        return account

    def read(self, account_id) -> Account:
        cg_from_db: Account = self.session.query(Account).filter(Account.id == account_id).first()
        self.session.commit()  # !TODO: костыль
        return cg_from_db

    def delete(self, account_id) -> None:
        self.session.query(Account).filter(Account.id == account_id).delete()
        self.session.commit()

