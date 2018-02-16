#!/usr/bin/env python

import logging
import sys

import aiocron

from assistant import core
from assistant.telegram import bot

logger = logging.getLogger(__name__)


@aiocron.crontab('30 9 * * 1-5', start=False)
async def notify_morning_weather():
    logger.info('Notify morning weather')
    for user_id in core.NOTIFICATION_CONSUMERS:
        try:
            private = bot.private(user_id)
            message = await core.weather()
            await private.send_text('Доброе утро!')
            await private.send_text(message)
            message = await core.wallets(core.ETH_WALLETS)
            await private.send_text(message)
        except Exception as e:
            logger.exception(e)


@aiocron.crontab('00 21 * * 1-5', start=False)
async def notify_money_rates():
    logger.info('Notify money rate')
    for user_id in core.NOTIFICATION_CONSUMERS:
        try:
            private = bot.private(user_id)
            message = await core.rates('Курсы валют на конец дня')
            await private.send_text(message)
            message = await core.wallets(core.ETH_WALLETS)
            await private.send_text(message)
        except Exception as e:
            logger.exception(e)


async def main():
    try:
        notify_morning_weather.start()
        notify_money_rates.start()
    except Exception as e:
        logger.exception(e)
        sys.exit(1)


def stop():
    notify_morning_weather.stop()
    notify_money_rates.stop()
