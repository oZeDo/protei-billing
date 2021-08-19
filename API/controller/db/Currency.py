from models.database.reflected_db import Currency, Companyrole
from models.database.sequencies import currency_id_seq
from API.controller.db.base import BaseDBController
from lib.utils import Fake
import random
import string


fake = Fake()


class CurrencyDBController(BaseDBController):
    def create(self) -> Currency:
        code = ''.join([random.choice(string.ascii_letters + string.digits + string.punctuation) for n in range(3)])
        currency = Currency(id=currency_id_seq.next_value(),
                            name=fake.currency_name(),
                            code=code,
                            baserate=1,
                            precision=2,
                            displayorder=self.session.query(Companyrole.id).count())
        self.session.add(currency)
        self.session.commit_changes()
        return currency

    def read(self, currency_id) -> Currency:
        cg_from_db: Currency = self.session.query(Currency).filter(Currency.id == currency_id).first()
        self.session.commit()  # !TODO: костыль
        return cg_from_db

    def delete(self, currency_id) -> None:
        self.session.query(Currency).filter(Currency.id == currency_id).delete()
        self.session.commit()

