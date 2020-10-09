#!/usr/bin/env python
import os
import re
from dataclasses import dataclass, field
from decimal import Decimal

import aiohttp
from aiohttp_socks import SocksConnector

SOCKS5_PROXY_URL = os.environ.get('SOCKS5_PROXY_URL', '')


def split(value: str):
    return [i.strip() for i in value.split(',') if i.strip()]


def create_proxy_session():
    connector = SocksConnector.from_url(SOCKS5_PROXY_URL)
    return aiohttp.ClientSession(connector=connector)


def cycle_day_left(start, datetime, cycle=4, shift=0):
    delta = start - datetime.date()
    return (delta.days + shift) % cycle


def plural_days(n):
    days = ('день', 'дня', 'дней',)

    if n % 10 == 1 and n % 100 != 11:
        p = 0
    elif 2 <= n % 10 <= 4 and (n % 100 < 10 or n % 100 >= 20):
        p = 1
    else:
        p = 2

    return str(n) + ' ' + days[p]


def parse_money(text: str):
    amount = re.findall(r'[\d.,]+', text)[0].replace(',', '.')

    def _text_contains(*items):
        return any(i in text.upper() for i in items)

    if _text_contains('$', 'USD'):
        return Decimal(amount), 'USD'
    if _text_contains('€', 'EUR'):
        return Decimal(amount), 'EUR'
    return Decimal(amount), None


def parse_temperature(text: str):
    return ''.join(re.findall(r'[-\d]', text))


@dataclass
class Storage:
    tickets: set = field(default_factory=set)
