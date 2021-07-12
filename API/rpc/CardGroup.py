from config.xgate_consts import XGATE_URL

from lib.net.request import http_post_request
from lib.utils import get_result
from models.services.card_group import CardGroup


class CardGroupAPI:

    def __init__(self):
        self.CARD_GROUP_SERVICE = '/card_group_service?'

    def create(self, model: CardGroup, *, root='cardGroup'):
        url = ''.join([XGATE_URL, self.CARD_GROUP_SERVICE, 'method=create_group'])
        response = http_post_request(url=url, data=model.to_xml(root=root)).text
        #!TODO вынести в отдельный метод
        try:
            model = CardGroup.from_dict(get_result(response)['resultObject'])
            return model
        except KeyError:
            return get_result(response)

    def read(self, group_id: str, include_card_ids: bool = False):
        url = ''.join([XGATE_URL, self.CARD_GROUP_SERVICE, 'method=get_group_by_id'])
        response = http_post_request(url=url, params={'group_id': group_id, 'include_card_ids': include_card_ids}).text
        try:
            model = CardGroup.from_dict(get_result(response)['resultObject'])
            return model
        except KeyError:
            return get_result(response)

    def update(self, model: CardGroup, *, root='cardGroup'):
        url = ''.join([XGATE_URL, self.CARD_GROUP_SERVICE, 'method=update_group'])
        response = http_post_request(url=url, data=model.to_xml(root=root)).text
        try:
            model = CardGroup.from_dict(get_result(response)['resultObject'])
            return model
        except KeyError:
            return get_result(response)

    def delete(self, group_id: str, include_card_ids: bool = False):
        url = ''.join([XGATE_URL, self.CARD_GROUP_SERVICE, 'method=delete_group_by_id'])
        response = http_post_request(url=url, params={'group_id': group_id, 'include_card_ids': include_card_ids}).text
        try:
            model = CardGroup.from_dict(get_result(response)['resultObject'])
            return model
        except KeyError:
            return get_result(response)
