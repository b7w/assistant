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
        except Exception as e:
            logger.exception(e)

    signal.signal(signal.SIGINT, stop)

    loop = asyncio.get_event_loop()
    loop.create_task(telegram.main())
    loop.create_task(cron.main())
    loop.run_forever()


if __name__ == '__main__':
    main()
