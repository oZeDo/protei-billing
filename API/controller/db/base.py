from API.controller.base import BaseController
from API.transport.db import DBSession


class BaseDBController(BaseController):
    @property
    def session(self):
        return self.__transport

    def __init__(self, url: str, pool_size: int, max_overflow: int):
        self.__transport = DBSession(url=url,
                                     pool_size=pool_size,
                                     max_overflow=max_overflow)
