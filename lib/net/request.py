# -*- coding: utf-8 -*-
from datetime import datetime

from typing import Any
from requests import post, get

from config.log_consts import LOG_HTTP_TRAFFIC
from lib.logger import Logger
from lib.utils import log_http_request

from lib.helpers.common import convert_to_md5
from config.xgate_consts import DEFAULT_USER, DEFAULT_PASSWORD, DEFAULT_INITIATOR


__logger = Logger("Requests lib").get()


def __make_cookies_header(cookies):
    return ';'.join([x + '=' + cookies[x] for x in cookies])


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


def http_get_request(url: str, params: dict = None, headers: dict = None, cookies: dict = None):
    """
    Send http GET request
    :param url: Server url without http prefix
    :param params: (optional) Params to urlencode
    :param headers: (optional) Set request headers
    :param cookies: (optional) Set request cookies
    :return: Full response
    """

    if headers is None:
        headers = {
            "Content-Type": "application/xml"
        }

    if cookies is not None:
        headers['Cookie'] = __make_cookies_header(cookies)

    __request_url = f"http://{url}"

    get_request = get(url=__request_url, params=params)

    if LOG_HTTP_TRAFFIC:
        log_http_request(__logger, get_request)

    get_request.raise_for_status()

    return get_request


def http_post_request(url: str, data: Any = None, params: dict = None, headers: dict = None, cookies: dict = None):
    """
    Send http POST request
    :param url: Server url without http prefix
    :param data: (optional) Dictionary, list of tuples, bytes, or file-like object to send in the body of the :class:`Request`.
    :param params: (optional) Params to urlencode
    :param headers: (optional) Set request headers
    :param cookies: (optional) Set request cookies. Default will be used if not given
    :return:
    """
    if headers is None:
        headers = {
            "Content-Type": "application/xml",
        }
        headers.update(make_auth_headers())

    if cookies is not None:
        headers['Cookie'] = __make_cookies_header(cookies)

    __request_url = f"http://{url}"

    post_request = post(url=__request_url, data=data, params=params, headers=headers)

    if LOG_HTTP_TRAFFIC:
        log_http_request(__logger, post_request)

    post_request.raise_for_status()

    return post_request
