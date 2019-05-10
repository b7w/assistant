#!/usr/bin/env python

import asyncio
import logging
import signal
from logging.config import dictConfig

from assistant import cron
from assistant import telegram

logger = logging.getLogger('root')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(levelname)-5s [%(asctime)s, %(msecs)d] %(name)s.%(funcName)s at %(lineno)d: %(message)s',
            'datefmt': '%Y-%b-%d %H:%M:%S',
        },
    },
    'handlers': {
        'simple': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        'asyncio': {
            'handlers': ['simple'],
            'level': 'DEBUG',
        },
        'aiotg': {
            'handlers': ['simple'],
            'level': 'DEBUG',
        },
        'assistant': {
            'handlers': ['simple'],
            'level': 'DEBUG',
        },
        'root': {
            'handlers': ['simple'],
            'level': 'DEBUG',
        },
    },
}


def main():
    dictConfig(LOGGING)
    logger.info('Starting app')

    def stop():
        try:
            logger.info("Stopping app..")
            telegram.stop()
            cron.stop()
            loop.stop()
        except Exception as e:
            logger.info(str(e))

    loop = asyncio.get_event_loop()
    loop.add_signal_handler(signal.SIGINT, stop)
    loop.add_signal_handler(signal.SIGTERM, stop)
    loop.create_task(telegram.main())
    loop.create_task(cron.main())
    try:
        loop.run_forever()
    finally:
        loop.close()
    logger.info("Bye!")


if __name__ == '__main__':
    main()
