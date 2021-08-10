from API.controller.base import BaseController
from API.transport.http import HTTPRequest
from lib.types import TransportParams
from lib.utils import make_cookies_header, make_auth_headers


class BaseRPCController(BaseController):

    @property
    def session(self) -> HTTPRequest.ClientType:
        return self.__session

    def __init__(self, base_url, endpoint, headers=None, cookies=None):
        if headers is None:
            headers = {
                "Content-Type": "application/xml"
            }
            headers.update(make_auth_headers())
        if cookies is not None:
            headers['Cookie'] = make_cookies_header(cookies)
        self.__session = HTTPRequest(TransportParams(base_url=base_url, endpoint=endpoint, headers=headers,
                                                     cookies=cookies)).client
