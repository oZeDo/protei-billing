import xmltodict
import re
from config.xgate_consts import XGATE_URL
from lib.net.request import http_post_request
from lib.utils import get_result
from models.services.card import Card, CardStateInfo, Lang, ReplaceCardResult, FailedCards, HLRProfileInfo,\
    HLRRegistrationInfo, Entry, Results, ActualCardStateInfo


class CardAPI:
    CARD = '/card_service'

    def __init__(self, model: Card = Card(), **kwargs: str):
        self.MSISDN = model.to_dict().get("msisdn") or kwargs.get("msisdn")
        self.IMSI = model.to_dict().get("imsi") or kwargs.get("imsi")

    def block(self):
        assert self.MSISDN, "msisdn is not specified"
        url = f"{XGATE_URL}{self.CARD}?method=block_sim_card&msisdn={self.MSISDN}"
        response = get_result(http_post_request(url=url).text)
        return response

    def legacy_block(self):
        assert self.IMSI and self.MSISDN, "imsi and msisdn is not specified"
        url = f"{XGATE_URL}{self.CARD}?method=self_block_sim_card&msisdn={self.MSISDN}&imsi={self.IMSI}"
        response = get_result(http_post_request(url=url).text)
        return response

    def unblock(self):
        assert self.MSISDN, "msisdn is not specified"
        url = f"{XGATE_URL}{self.CARD}?method=unblock_sim_card&msisdn={self.MSISDN}"
        response = get_result(http_post_request(url=url).text)
        return response

    def legacy_unblock(self):
        assert self.IMSI and self.MSISDN, "imsi and msisdn is not specified"
        url = f"{XGATE_URL}{self.CARD}?method=unblock_self_blocked_sim_card&msisdn={self.MSISDN}&imsi={self.IMSI}"
        response = get_result(http_post_request(url=url).text)
        return response

    def get_basic_info(self, iccid: str):
        assert self.MSISDN, "msisdn is not specified"
        url = f"{XGATE_URL}{self.CARD}?method=get_card_basic_info&msisdn={self.MSISDN}"
        params = {
            "iccid": iccid
        }
        response = get_result(http_post_request(url=url, params=params).text)
        if response["status"] == "OK":
            return Card.from_dict(response['resultObject'])
        return response

    def get_state_info(self, url=''):
        assert self.MSISDN, "msisdn is not specified"
        url = f"{XGATE_URL}{self.CARD}?method=get_card_state_info{url}&msisdn={self.MSISDN}"
        response = get_result(http_post_request(url=url).text)
        if response["status"] == "OK":
            if not response["resultObject"]["cardOperativeStateChangeHistory"]:
                print("Тэг неправильно открыт/закрыт")
                response["resultObject"]["cardOperativeStateChangeHistory"] = []
            return CardStateInfo.from_dict(response['resultObject'])
        return response

    def get_state_info_no_pinpuk(self):
        return self.get_state_info("_without_pinpuk")

    def change_number_status(self, status_id: int):
        assert self.MSISDN, "msisdn is not specified"
        url = f"{XGATE_URL}{self.CARD}?method=change_number_status&msisdn={self.MSISDN}"
        params = {
            "status_id": status_id
        }
        response = get_result(http_post_request(url=url, params=params).text)
        return response

    def change_msisdn(self, new_msisdn: str, no_sold_card: bool = False, free_old_msisdn: bool = False):
        assert self.MSISDN, "msisdn is not specified"
        url = f"{XGATE_URL}{self.CARD}?method=change_msisdn"
        params = {
            "old_msisdn": self.MSISDN,
            "new_msisdn": new_msisdn,
            "no_sold_card": no_sold_card,
            "free_old_msisdn": free_old_msisdn
            }
        response = get_result(http_post_request(url=url, params=params).text)
        return response

    def delete_list(self, card_list: list):
        url = f"{XGATE_URL}{self.CARD}?method=delete_card_list"
        data = f"<list>{''.join([f'<long>{i}</long>' for i in card_list])}<list>"
        response = get_result(http_post_request(url=url, data=data).text)
        return response

    def change_lang(self, lang_id: int):
        url = f"{XGATE_URL}{self.CARD}?method=change_lang&msisdn={self.MSISDN}"
        params = {
            "lang_id": lang_id
        }
        response = get_result(http_post_request(url=url, params=params).text)
        return response

    def repair(self, card_id: int, disable_desynched: bool = False):
        url = f"{XGATE_URL}{self.CARD}?method=repair_sim_card&msisdn={self.MSISDN}"
        params = {
            "card_id": card_id,
            "disable_desynched": disable_desynched
        }
        response = get_result(http_post_request(url=url, params=params).text)
        return response

    def get_all(self):
        assert self.IMSI, "imsi is not specified"
        url = f"{XGATE_URL}{self.CARD}?method=get_all_msisdn&imsi={self.IMSI}"
        response = get_result(http_post_request(url=url).text)
        if response["status"] == "OK":
            return [i for i in re.findall("<msisdn>(.*?)</msisdn>", response['resultObject'])]
        return response

    def get_lang(self):
        assert self.MSISDN, "msisdn is not specified"
        url = f"{XGATE_URL}{self.CARD}?method=get_lang&msisdn={self.MSISDN}"
        response = get_result(http_post_request(url=url).text)
        if response["status"] == "OK":
            return Lang.from_dict(response['resultObject'])
        return response

    def replace(self, new_imsi: str):   # need to test
        assert self.MSISDN, "msisdn is not specified"
        url = f"{XGATE_URL}{self.CARD}?method=replace_sim_card&msisdn={self.MSISDN}"
        params = {
            "new_imsi": new_imsi
        }
        response = get_result(http_post_request(url=url, params=params).text)
        if response["status"] == "OK":
            return ReplaceCardResult.from_dict(response['resultObject'])
        return response

    def change_client(self, client_id: int = None):   # need to test
        assert self.MSISDN, "msisdn is not specified"
        url = f"{XGATE_URL}{self.CARD}?method=change_client&msisdn={self.MSISDN}"
        params = {"client_id": client_id} if client_id is not None else {}
        response = get_result(http_post_request(url=url, params=params).text)
        return response

    def delete_list_extended(self, card_list: list):
        url = f"{XGATE_URL}{self.CARD}?method=delete_card_list_extended"
        data = f"<list>{''.join([f'<long>{i}</long>' for i in card_list])}<list>"  # <long>1</long> generator in <list>
        response = get_result(http_post_request(url=url, data=data).text)
        if response["status"] == "OK":
            return FailedCards.from_dict(response['resultObject'])
        return response

    def check_hlr(self):
        assert self.MSISDN and self.IMSI, "msisdn and imsi are not specified"
        url = f"{XGATE_URL}{self.CARD}?method=check_hlr_profile&msisdn={self.MSISDN}&imsi={self.IMSI}"
        response = get_result(http_post_request(url=url).text)
        if response["status"] == "OK":
            return HLRProfileInfo.from_dict(response['resultObject'])
        return response

    def change_check_state(self, check_state_id: int):
        assert self.MSISDN, "msisdn is not specified"
        url = f"{XGATE_URL}{self.CARD}?method=change_check_state&msisdn={self.MSISDN}"
        params = {
            "check_state_id": check_state_id
        }
        response = get_result(http_post_request(url=url, params=params).text)
        return response

    def free_number(self):
        assert self.MSISDN, "msisdn is not specified"
        url = f"{XGATE_URL}{self.CARD}?method=free_number&msisdn={self.MSISDN}"
        response = get_result(http_post_request(url=url).text)
        return response

    def get_hlr(self):
        assert self.MSISDN, "msisdn is not specified"
        url = f"{XGATE_URL}{self.CARD}?method=get_hlr_registration_info&msisdn={self.MSISDN}"
        response = get_result(http_post_request(url=url).text)
        if response["status"] == "OK":
            return HLRRegistrationInfo.from_dict(response['resultObject'])
        return response

    def imsi_or_msisdn(self, url):
        """
        Assigns imsi or\and msisdn if they exist. And checks if they are present in final url
        :param url: a url method without params
        :return: url with required params
        """
        url = url + f"&msisdn={self.MSISDN}" if self.MSISDN else url
        url = url + f"&imsi={self.IMSI}" if self.IMSI else url
        assert ("imsi" in url) or ("msisdn" in url), "Imsi or\\and msisdn are not specified"
        return url

    def change_info(self, user_name: str, info: str, info2: str, ignore_null_values: bool = True):  # Additional Check!!
        url = self.imsi_or_msisdn(f"{XGATE_URL}{self.CARD}?method=change_card_info")
        params = {
            "user_name": user_name,
            "info": info,
            "info2": info2,
            "ignore_null_values": ignore_null_values
            }
        response = get_result(http_post_request(url=url, params=params).text)
        return response

    def activate(self):
        url = self.imsi_or_msisdn(f"{XGATE_URL}{self.CARD}?method=card_activation")
        response = get_result(http_post_request(url=url).text)
        return response

    def enable_money_counter(self, limit: float, enable_notification: bool = None):
        url = self.imsi_or_msisdn(f"{XGATE_URL}{self.CARD}?method=enable_card_money_counter")
        params = {
            "limit": round(limit, 2)
        }
        if enable_notification:
            params.update({"enable_notification": enable_notification})
        response = get_result(http_post_request(url=url, params=params).text)
        return response

    def disable_money_counter(self):
        url = self.imsi_or_msisdn(f"{XGATE_URL}{self.CARD}?method=disable_card_money_counter")
        response = get_result(http_post_request(url=url).text)
        return response

    def get_money_counter(self, card_list: list):   # not done. Need more examples of list
        url = f"{XGATE_URL}{self.CARD}?method=get_card_money_counter_infos"
        data = f"<list>{''.join([f'<long>{i}</long>' for i in card_list])}<list>"  # <long>1</long> generator in <list>
        response = get_result(http_post_request(url=url, data=data).text)
        if response["status"] == "OK":
            return Entry.from_dict(response['resultObject'])
        return response

    def get_inactive_cards(self, card_list: list, inaccuracy_percent: int, startLast_activity: str,
                           virtual_group_id: int, client_id: int, page_size: int, page_num: int):
        url = f"{XGATE_URL}{self.CARD}?method=get_potentially_inactive_cards"
        tmp = f"<cardIds>{''.join([f'<long>{i}</long>' for i in card_list])}</cardIds>"
        data = f"<cardActivityFilter><inaccuracyPercent>{inaccuracy_percent}</inaccuracyPercent>" \
               f"<startLastActivity>{startLast_activity}</startLastActivity>{tmp}" \
               f"<virtualGroupId>{virtual_group_id}</virtualGroupId><clientId>{client_id}</clientId>" \
               f"</cardActivityFilter>"
        params = {
            "page_size": page_size,
            "page_num": page_num
        }
        response = get_result(http_post_request(url=url, data=data, params=params).text)
        if response["status"] == "OK":
            return Results.from_dict(response['resultObject'])
        return response

    def phone_number_transfer(self, card_id: int):
        url = f"{XGATE_URL}{self.CARD}?method=phone_number_transfer"
        params = {
            "card_id": card_id
        }
        response = get_result(http_post_request(url=url, params=params).text)
        return response

    def get_state_with_invoices(self):  # ? journal
        url = self.imsi_or_msisdn(f"{XGATE_URL}{self.CARD}?method=get_card_state_info_with_invoices")
        response = get_result(http_post_request(url=url).text)
        if response["status"] == "OK":
            return ActualCardStateInfo.from_dict(response['resultObject'])
        return response


if __name__ == "__main__":
    a = {'iccid': '89791300000000', 'msisdn': '79130000000', 'imsi': '250470091300000', 'cardId': '36911'}

    t = Card(**a)
    api = CardAPI(model=t)
    # print(api.IMSI)
    print(api.get_state_info())
    # print(api.replace("250000000000000000"))
