from httpx import Client, Limits, HTTPTransport

from lib.types import TransportParams


class HTTPRequest:
    """Synchronous http client with params persistence"""
    ClientType = Client

    def __init__(self, params: TransportParams, *,
                 max_keepalive_connections=10,
                 max_connections=10,
                 auth=None,
                 transport=HTTPTransport(),
                 event_hooks=None):
        self.__limits = Limits(max_keepalive_connections=max_keepalive_connections,
                               max_connections=max_connections)
        self.__auth = auth  # Можно свое
        self.__transport = transport
        self.__client = Client(headers=params.headers,
                               base_url=params.base_url,
                               cookies=params.cookies,
                               event_hooks=event_hooks,
                               limits=self.__limits,
                               transport=self.__transport,
                               auth=self.__auth)

    @property
    def client(self):
        return self.__client
