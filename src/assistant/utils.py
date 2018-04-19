#!/usr/bin/env python
import os

import aiohttp
from aiosocks import Socks5Auth
from aiosocks.connector import ProxyClientRequest, ProxyConnector
from yarl import URL

SOCKS5_PROXY_URL = os.environ['SOCKS5_PROXY_URL']
SOCKS5_PROXY_CREDENTIALS = os.environ['SOCKS5_PROXY_CREDENTIALS']


class PermanentProxyClientRequest(ProxyClientRequest):

    def update_proxy(self, proxy, proxy_auth, proxy_headers):
        super().update_proxy(proxy, proxy_auth, proxy_headers)
        self.proxy = URL('socks5://' + SOCKS5_PROXY_URL)
        login, password = SOCKS5_PROXY_CREDENTIALS.split(':')
        self.proxy_auth = Socks5Auth(login, password)


def create_proxy_session():
    conn = ProxyConnector(remote_resolve=True)
    return aiohttp.ClientSession(connector=conn, request_class=PermanentProxyClientRequest)
