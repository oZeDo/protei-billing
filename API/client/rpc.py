from API.controller.rpc.CardGroup import CardGroupController
from API.controller.rpc.Card import CardController
from config.xgate_consts import XGATE_URL


class RPCClient:
    def __init__(self, url=XGATE_URL):
        self.card_group = CardGroupController(base_url=url, endpoint='')
        self.card = CardController(base_url=url, endpoint='')
