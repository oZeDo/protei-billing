import warnings
from API.controller import BaseRPCController
from models.services.card import Long


class CardController(BaseRPCController):
    SERVICE_URL = '/card_service?'

    def block_sim_card(self, msisdn: str):
        params = {
            "msisdn": msisdn,
        }
        return self.session.post(url=self.SERVICE_URL + "method=block_sim_card", params=params)

    def self_block_sim_card(self, msisdn: str, imsi: str):
        params = {
            "msisdn": msisdn,
            "imsi": imsi
        }
        return self.session.post(url=self.SERVICE_URL + "method=self_block_sim_card", params=params)

    def unblock_sim_card(self, msisdn: str):
        params = {
            "msisdn": msisdn
        }
        return self.session.post(url=self.SERVICE_URL + "method=unblock_sim_card", params=params)

    def unblock_self_blocked_sim_card(self, msisdn: str, imsi: str):
        params = {
            "msisdn": msisdn,
            "imsi": imsi
        }
        return self.session.post(url=self.SERVICE_URL + "method=unblock_self_blocked_sim_card", params=params)

    def get_card_basic_info(self, msisdn: str, iccid: str):
        params = {
            "msisdn": msisdn,
            "iccid": iccid
        }
        return self.session.post(url=self.SERVICE_URL + "method=get_card_basic_info", params=params)

    def get_cards_basic_info(self, imei: str):
        params = {
            "imei": imei,
        }
        return self.session.post(url=self.SERVICE_URL + "method=get_cards_basic_info", params=params)

    def get_card_basic_info_with_paging(self, client_id: int, dealer_id: int, page_size: int, page_num: int):
        # !TODO: Выяснить какие из параметров mandatory
        params = {
            "client_id": client_id,
            "dealer_id": dealer_id,
            "page_size": page_size,
            "page_num": page_num,
        }
        return self.session.post(url=self.SERVICE_URL + "method=get_card_basic_info_with_paging", params=params)

    def get_card_state_info_without_pinpuk(self, msisdn: str):
        params = {
            "msisdn": msisdn,
        }
        return self.session.post(url=self.SERVICE_URL + "method=get_card_state_info_without_pinpuk", params=params)

    def change_number_status(self, msisdn: str, status_id: int):
        params = {
            "msisdn": msisdn,
            "status_id": status_id
        }
        return self.session.post(url=self.SERVICE_URL + "method=change_number_status", params=params)

    def change_msisdn(self, old_msisdn: str, new_msisdn: str, *, no_sold_card: bool = False,
                      free_old_msisdn: bool = False):
        params = {
            "old_msisdn": old_msisdn,
            "new_msisdn": new_msisdn,
            "no_sold_card": no_sold_card,
            "free_old_msisdn": free_old_msisdn
        }
        return self.session.post(url=self.SERVICE_URL + "method=change_msisdn", params=params)

    def delete_card(self, card_id: int):
        params = {
            "card_id": card_id,
        }
        return self.session.post(url=self.SERVICE_URL + "method=delete_card", params=params)

    def change_lang(self, msisdn: str, lang_id: int):
        params = {
            "msisdn": msisdn,
            "lang_id": lang_id
        }
        return self.session.post(url=self.SERVICE_URL + "method=change_lang", params=params)

    def repair_sim_card(self, msisdn: str, card_id: int):
        params = {
            "msisdn": msisdn,
            "card_id": card_id
        }
        return self.session.post(url=self.SERVICE_URL + "method=repair_sim_card", params=params)

    def get_all_msisdn(self, imsi: str):
        params = {
            "imsi": imsi
        }
        return self.session.post(url=self.SERVICE_URL + "method=get_all_msisdn", params=params)

    def get_lang(self, msisdn: str):
        params = {
            "msisdn": msisdn
        }
        return self.session.post(url=self.SERVICE_URL + "method=get_lang", params=params)

    def replace_sim_card(self, msisdn: str, new_imsi: str):  # need to test
        params = {
            "msisdn": msisdn,
            "new_imsi": new_imsi
        }
        return self.session.post(url=self.SERVICE_URL + "method=replace_sim_card", params=params)

    def change_client(self, msisdn: str, client_id: int):  # need to test
        params = {
            "msisdn": msisdn,
            "client_id": client_id
        }
        return self.session.post(url=self.SERVICE_URL + "method=change_client", params=params)

    def delete_card_list_extended(self, model: Long, *, root="list"):
        return self.session.post(url=self.SERVICE_URL + "method=delete_card_list_extended",
                                 data=model.to_xml(root=root))

    def change_check_state(self, msisdn: str, check_state_id: int):
        params = {
            "msisdn": msisdn,
            "check_state_id": check_state_id
        }
        return self.session.post(url=self.SERVICE_URL + "method=change_check_state", params=params)

    def free_number(self, msisdn: str):
        params = {
            "msisdn": msisdn
        }
        return self.session.post(url=self.SERVICE_URL + "method=free_number", params=params)

    def get_hlr_registration_info(self, msisdn: str):
        params = {
            "msisdn": msisdn
        }
        return self.session.post(url=self.SERVICE_URL + "method=get_hlr_registration_info", params=params)

    # Ушло в Сервис по работе провижинингом ??????????
    # def get_hlr_registration_info(self, msisdn: str):
    #     params = {
    #         "msisdn": msisdn
    #     }
    #     return self.session.post(url=self.SERVICE_URL + "method=get_hlr_registration_info", params=params)

    def change_card_info(self, user_name: str, info: str, info2: str, ignore_null_values: bool = True,
                         msisdn: str = None, imsi: str = None):
        if not imsi and not msisdn:
            warnings.warn("Не заданы imsi и\\или msisdn")
        params = {
            "msisdn": msisdn,
            "imsi": imsi,
            "user_name": user_name,
            "info": info,
            "info2": info2,
            "ignore_null_values": ignore_null_values
        }
        return self.session.post(url=self.SERVICE_URL + "method=change_card_info", params=params)

    def card_activation(self, msisdn: str = None, imsi: str = None):
        if not imsi and not msisdn:
            warnings.warn("Не заданы imsi и\\или msisdn")
        params = {
            "msisdn": msisdn,
            "imsi": imsi
        }
        return self.session.post(url=self.SERVICE_URL + "method=card_activation", params=params)

    def enable_card_money_counter(self, limit: float, enable_notification: bool = None, msisdn: str = None,
                                  imsi: str = None):
        if not imsi and not msisdn:
            warnings.warn("Не заданы imsi и\\или msisdn")
        params = {
            "msisdn": msisdn,
            "imsi": imsi,
            "limit": limit,
            "enable_notification": enable_notification,
        }
        return self.session.post(url=self.SERVICE_URL + "method=enable_card_money_counter", params=params)

    def disable_card_money_counter(self, msisdn: str = None, imsi: str = None):
        if not imsi and not msisdn:
            warnings.warn("Не заданы imsi и\\или msisdn")
        params = {
            "msisdn": msisdn,
            "imsi": imsi,
        }
        return self.session.post(url=self.SERVICE_URL + "method=disable_card_money_counter", params=params)

    def get_card_money_counter_infos(self, model: Long, *, root="list"):
        return self.session.post(url=self.SERVICE_URL + "method=get_card_money_counter_infos",
                                 data=model.to_xml(root=root))

    # !TODO: Переделать data в model / Принимать на вход готовую модель?
    # https://wiki.protei.ru/doku.php?id=protei:cpe:billing:xgate:requests
    def get_potentially_inactive_cards(self, card_list: list, inaccuracy_percent: int, start_last_activity: str,
                                       virtual_group_id: int, client_id: int, page_size: int, page_num: int):
        tmp = f"<cardIds>{''.join([f'<long>{i}</long>' for i in card_list])}</cardIds>"
        data = f"<cardActivityFilter><inaccuracyPercent>{inaccuracy_percent}</inaccuracyPercent>" \
               f"<startLastActivity>{start_last_activity}</startLastActivity>{tmp}" \
               f"<virtualGroupId>{virtual_group_id}</virtualGroupId><clientId>{client_id}</clientId>" \
               f"</cardActivityFilter>"
        params = {
            "page_size": page_size,
            "page_num": page_num
        }
        return self.session.post(url=self.SERVICE_URL + "method=get_potentially_inactive_cards", params=params,
                                 data=data)

    def phone_number_transfer(self, card_id: int):
        # !TODO: В чем смысл метода???????????????????????????
        params = {
            "card_id": card_id
        }
        return self.session.post(url=self.SERVICE_URL + "method=phone_number_transfer", params=params)

    def get_card_state_info_with_invoices(self, msisdn: str = None, imsi: str = None):
        if not imsi and not msisdn:
            warnings.warn("Не заданы imsi и\\или msisdn")
        params = {
            "msisdn": msisdn,
            "imsi": imsi
        }
        return self.session.post(url=self.SERVICE_URL + "method=get_card_state_info_with_invoices", params=params)
