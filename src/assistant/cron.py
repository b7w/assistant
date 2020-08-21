#!/usr/bin/env python

import logging

import aiocron

from assistant import core
from assistant.telegram import bot

logger = logging.getLogger(__name__)


@aiocron.crontab('00 21 * * 1-5', start=False)
async def daily_notify():
    logger.info('Notify money rate')
    for user_id in core.NOTIFICATION_CONSUMERS:
        try:
            private = bot.private(user_id)
            message = await core.rates('Курсы валют на конец дня')
            await private.send_text(message)
            message = await core.workday()
            await private.send_text(message)
        except Exception as e:
            logger.exception(e)


@aiocron.crontab('0 8-22 * * *', start=False)
async def sechenov_tickets_notify():
    logger.debug('Notify sechenov tickets')
    for user_id in core.NOTIFICATION_CONSUMERS:
        try:
            private = bot.private(user_id)
            for doc in core.SECHENOV_DOCTORS:
                tickets = await core.sechenov_find_tickets(core.storage, doc)
                for link, text in tickets:
                    await private.send_text(f'{text}\n{link}')
        except Exception as e:
            logger.exception(e)


async def main():
    try:
        daily_notify.start()
        sechenov_tickets_notify.start()
    except Exception as e:
        logger.exception(e)
        raise e


def stop():
    daily_notify.stop()
    sechenov_tickets_notify.stop()
