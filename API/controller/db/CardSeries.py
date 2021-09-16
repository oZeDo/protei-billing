from models.database.reflected_db import Cardsery
from models.database.sequencies import card_series_id_seq
from API.controller.db.base import BaseDBController
from lib.utils import Fake

fake = Fake()


class CardSeriesDBController(BaseDBController):
    def create(self, currency_id, accounting_file_id, amount):
        new_card_series = Cardsery(id=card_series_id_seq.next_value(),
                                   name=fake.safe_color_name(),
                                   cardamount=amount,
                                   cardtype=1,
                                   seriesprefix=fake.uuid4(),
                                   currencyid=currency_id,
                                   accfileid=accounting_file_id)
        self.session.add(new_card_series)
        self.session.commit()
        return new_card_series

    def read(self, card_series_id):
        cg_from_db: Cardsery = self.session.query(Cardsery).filter(Cardsery.id == card_series_id).first()
        return cg_from_db

    def delete(self, card_series_id):
        self.session.query(Cardsery).filter(Cardsery.id == card_series_id).delete()
        self.session.commit()
