#!/usr/bin/env python
import os

import aiohttp
from aiohttp_socks import SocksConnector

SOCKS5_PROXY_URL = os.environ.get('SOCKS5_PROXY_URL', '')


def create_proxy_session():
    connector = SocksConnector.from_url(SOCKS5_PROXY_URL)
    return aiohttp.ClientSession(connector=connector)
