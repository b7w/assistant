#!/usr/bin/env python

import logging

import aiocron

from assistant import core
from assistant.telegram import bot

logger = logging.getLogger(__name__)


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
        notify_money_rates.start()
    except Exception as e:
        logger.exception(e)
        raise e


def stop():
    notify_money_rates.stop()
