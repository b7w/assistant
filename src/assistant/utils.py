#!/usr/bin/env python
import os

import aiohttp
from aiohttp_socks import SocksConnector

SOCKS5_PROXY_URL = os.environ.get('SOCKS5_PROXY_URL', '')


def create_proxy_session():
    connector = SocksConnector.from_url(SOCKS5_PROXY_URL)
    return aiohttp.ClientSession(connector=connector)


def is_cycle_day(start, datetime, cycle=4):
    delta = start - datetime.date()
    return delta.days % cycle == 0
