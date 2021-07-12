from lib.helpers.common import convert_to_md5
from config.xgate_consts import DEFAULT_USER, DEFAULT_PASSWORD, DEFAULT_INITIATOR


def make_auth_headers(user=None, password=None, initiator=None):

    if not user:
        user = DEFAULT_USER
    if not password:
        password = DEFAULT_PASSWORD
    if not initiator:
        initiator = DEFAULT_INITIATOR

    return {
        "X-Login": user,
        "X-Password": convert_to_md5(password),
        "X-ReqInitiator": initiator
    }

