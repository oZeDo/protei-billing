from API.controller.rpc.base import BaseRPCController
from models.services.card_group import CardGroup


class CardGroupController(BaseRPCController):
    SERVICE_URL = '/card_group_service?'

    def create(self, model: CardGroup, *, root='cardGroup'):
        return self.session.post(url=self.SERVICE_URL+"method=create_group", data=model.to_xml(root=root))

    def read(self, group_id: str, include_card_ids: bool = False):
        params = {
            'group_id': group_id,
            'include_card_ids': include_card_ids
        }
        return self.session.post(url=self.SERVICE_URL+"method=get_group_by_id", params=params)

    def update(self, model: CardGroup, *, root='cardGroup'):
        return self.session.post(url=self.SERVICE_URL + "method=update_group", data=model.to_xml(root=root))

    def delete(self, group_id: str, include_card_ids: bool = False):
        params = {
            'group_id': group_id,
            'include_card_ids': include_card_ids
        }
        return self.session.post(url=self.SERVICE_URL+"method=delete_group_by_id", params=params)
