from API.controller.db.CardGroup import CardGroupDBController
from API.controller.db.Client import ClientDBController
from API.controller.db.Card import CardDBController


class DBClient:
    def __init__(self, url: str, pool_size: int = 5, max_overflow: int = 5):
        """Database client, which provides access for all db controllers and methods.

        Args:
            url (str): Database connection string (DSN). Exmaple format: {DRIVER}://{USER}:{PASSWORD}@{HOST}:{PORT}/{SID}
            pool_size (int, optional): Number of connections to be maintained. Defaults to 5.
            max_overflow (int, optional): The maximum overflow size of the pool. Defaults to 5.
        """

        self.card_group = CardGroupDBController(url, pool_size, max_overflow)
        self.client = ClientDBController(url, pool_size, max_overflow)
        self.card = CardDBController(url, pool_size, max_overflow)
