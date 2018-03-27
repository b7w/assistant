#!/usr/bin/env python

import asyncio
import logging
import os
import pprint
import re
import tempfile
from decimal import Decimal

import aiohttp
import transmissionrpc
from parsel import Selector

logger = logging.getLogger(__name__)

NOTIFICATION_CONSUMERS = ["105720423"]
TORRENT_CONSUMERS = ["105720423"]
ETH_WALLETS = os.environ['ETH_WALLETS'].split(',')


async def _retrieve_rates():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://www.tinkoff.ru/api/v1/currency_rates/') as resp:
            logger.debug('GET https://www.tinkoff.ru/api/v1/currency_rates/ with status: %s', resp.status)
            data = await resp.json()
            return data['payload']['rates']


async def _retrieve_page(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            logger.debug('GET %s with status: %s', url, resp.status)
            data = await resp.text()
            return Selector(text=data)


def _find_rate(rates, from_name, to_name):
    for rate in rates:
        if rate['category'] == 'DebitCardsTransfers' and rate['fromCurrency']['name'] == from_name and \
            rate['toCurrency']['name'] == to_name:
            return (Decimal(rate['buy']) + Decimal(rate['sell'])) / 2


def find_rate(rates, from_name, to_name):
    rate = _find_rate(rates, from_name, to_name)
    if rate is None:
        rate = 1 / _find_rate(rates, to_name, from_name)
    return rate


async def _retrieve_yobit_rates():
    url = 'https://yobit.io/api/3/ticker/eth_usd-etz_usd-xem_eth-xem_usd-btc_usd'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            logger.debug('GET %s with status: %s', url, resp.status)
            res = await resp.json(content_type='text/html')
            for pair in res.values():
                del pair['updated']
                del pair['buy']
                del pair['sell']
                del pair['vol_cur']
            return res


async def _retrieve_eth_wallet_balance(address):
    url = 'https://ethplorer.io/service/service.php?data={}'.format(address)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            logger.debug('GET %s with status: %s', url, resp.status)
            data = await resp.json(content_type='text/html')
            return Decimal(data['balance'])


async def rates(header='Курсы валют'):
    rates = await _retrieve_rates()
    usd = find_rate(rates, 'USD', 'RUB')
    eur = find_rate(rates, 'EUR', 'RUB')
    rates = await _retrieve_yobit_rates()
    yobit = {k: Decimal(v['avg']) for k, v in rates.items()}
    return f'{header}\n' \
           f'USD: {usd:.2f}\n' \
           f'EUR: {eur:.2f}\n' \
           f'BTC/USD: {yobit["btc_usd"]:.2f}\n' \
           f'ETZ/USD: {yobit["etz_usd"]:.2f}\n' \
           f'ETH/USD: {yobit["eth_usd"]:.2f}\n' \
           f'XEM/USD: {yobit["xem_usd"]:.2f}\n' \
           f'XEM/ETH: {yobit["xem_eth"]:.8f}'


async def yobit():
    data = await _retrieve_yobit_rates()
    return 'Yobit\n' + pprint.pformat(data)


def parse_money(text: str):
    amount = ''.join(re.findall(r'\d', text))

    def _text_contains(*items):
        return any(i in text.upper() for i in items)

    if _text_contains('$', 'USD'):
        return int(amount), 'USD'
    if _text_contains('€', 'EUR'):
        return int(amount), 'EUR'
    return int(amount), None


def _currency_calculator(rates, amount, from_currency, to_currency='RUB'):
    rate = find_rate(rates, from_currency, to_currency)
    total = round(rate * amount)
    return f'{amount} {from_currency} = {total} {to_currency}'


async def currency_calculator(amount, currency):
    rates = await _retrieve_rates()
    currencies = [(currency, 'RUB')] if currency else [('USD', 'RUB',),
                                                       ('EUR', 'RUB',),
                                                       ('RUB', 'USD',),
                                                       ('RUB', 'EUR'), ]
    return '\n'.join(_currency_calculator(rates, amount, f, s) for f, s in currencies)


def _extract_number(page, query):
    number_pattern = r'[-+' + chr(8722) + ']?\d+'
    value = page.css(query).re_first(number_pattern)
    return value.replace(chr(8722), '-')


async def weather():
    page = await _retrieve_page('https://yandex.ru/pogoda/moscow/')

    temp = page.css('.fact__temp .temp__value::text').extract_first()
    comment = page.css('.day-anchor::text').extract_first()
    feels_like = page.css('.fact__feels-like .temp__value::text').extract_first()
    yesterday = page.css('.fact__yesterday .temp__value::text').extract_first()

    return f'Сейчас в Москве {comment}, ' \
           f'Температура {temp}°C\n' \
           f'Ощущается как {feels_like}°C\n' \
           f'Вчера в это время {yesterday}°C'


async def add_torrent(bot, document):
    file_name = document['file_name']
    info = await bot.get_file(document['file_id'])
    async with bot.download_file(info['file_path']) as r:
        content = await r.read()

        def blocking():
            with tempfile.NamedTemporaryFile() as f:
                f.write(content)
                f.flush()
                address, user, password = os.environ['TRANSMISSION_URL'].split(':')
                client = transmissionrpc.Client(address=address, user=user, password=password)
                tr = client.add_torrent('file://' + f.name, download_dir='/media/torrents/Movie')
                logger.debug('Add torrent "%s" with id %s', file_name, tr.id)
                return 'Done'

        return await asyncio.get_event_loop().run_in_executor(None, blocking)


async def wallets(addresses):
    message = 'Ethereum кошельки\n'
    for adr in addresses:
        bal = await _retrieve_eth_wallet_balance(adr)
        yobit = await _retrieve_yobit_rates()
        rate = Decimal(yobit['eth_usd']['avg'])
        bal_usd = bal * rate
        message += f'{adr[:8]}  ETH: {bal:.4f} USD: {bal_usd:.2f} USD/EHT: {rate:.2f}\n'
    return message
