#!/usr/bin/env python

import logging
import os
from decimal import Decimal

from aiotg import Bot, Chat

from assistant import core
from assistant.utils import create_proxy_session

bot = Bot(os.environ['TELEGRAM_BOT_TOKEN'])

logger = logging.getLogger(__name__)


@bot.command("start")
async def help(chat: Chat, match):
    logger.debug('chat: %s, command: help', chat.id)
    help = ("rates - Tinkoff currency rate\n"
            "rate - Currency calculator\n"
            "weather - Current temperature\n"
            "wallets - Wallets\n"
            "yobit - Yobit\n"
            "workday - Workday\n"
            "report - Combine all commands")
    await chat.send_text(help.strip(''))


@bot.command("rate (.+)")
async def rate(chat: Chat, match):
    logger.debug('chat: %s, command: rate', chat.id)
    try:
        amount, currency = core.parse_money(match.group(1))
        message = await core.currency_calculator(Decimal(amount), currency)
        await chat.send_text(message)
    except Exception as e:
        logger.exception(e)
        await chat.send_text('System error')


@bot.command("rates")
async def rates(chat: Chat, match):
    logger.debug('chat: %s, command: rates', chat.id)
    try:
        message = await core.rates()
        await chat.send_text(message)
    except Exception as e:
        logger.exception(e)
        await chat.send_text('System error')


@bot.command("weather")
async def weather(chat: Chat, match):
    logger.debug('chat: %s, command: weather', chat.id)
    try:
        message = await core.yandex_weather()
        await chat.send_text(message)
    except Exception as e:
        logger.exception(e)
        await chat.send_text('System error')


@bot.command("wallets")
async def wallets(chat: Chat, match):
    logger.debug('chat: %s, command: wallets', chat.id)
    try:
        message = await core.wallets(core.ETH_WALLETS)
        await chat.send_text(message)
    except Exception as e:
        logger.exception(e)
        await chat.send_text('System error')


@bot.command("yobit")
async def yobit(chat: Chat, match):
    logger.debug('chat: %s, command: yobit', chat.id)
    try:
        message = await core.yobit()
        await chat.send_text(message)
    except Exception as e:
        logger.exception(e)
        await chat.send_text('System error')


@bot.command("workday")
async def workday(chat: Chat, match):
    logger.debug('chat: %s, command: workday', chat.id)
    try:
        message = core.workday()
        await chat.send_text(message)
    except Exception as e:
        logger.exception(e)
        await chat.send_text('System error')


@bot.command("report")
async def report(chat: Chat, match):
    logger.debug('chat: %s, command: report', chat.id)
    await weather(chat, match)
    await rates(chat, match)
    await wallets(chat, match)
    await workday(chat, match)


@bot.handle('document')
async def file_handler(chat, document):
    logger.debug('chat: %s, command: file_handler', chat.id)
    try:
        if str(chat.sender['id']) in core.TORRENT_CONSUMERS:
            result = await core.add_torrent(bot, document)
            await chat.send_text(str(result))
        else:
            logger.info('file_handler not allowed for %s', chat.sender)
    except Exception as e:
        logger.exception(e)
        await chat.send_text('System error')


@bot.default
async def default(chat, message):
    logger.debug('Default command, chat: %s message: %s', chat, message)
    await chat.send_text('Unknown command, try /start for help')


async def main():
    try:
        bot._session = create_proxy_session()
        await bot.loop()
    except Exception as e:
        logger.exception(e)
        raise e


def stop():
    bot.stop()
