import asyncio
import logging
import unittest
from logging.config import dictConfig

from assistant import core
from assistant.tests import LOGGING

logger = logging.getLogger(__name__)


class TestWeather(unittest.TestCase):
    def setUp(self):
        dictConfig(LOGGING)
        self.loop = asyncio.get_event_loop()

    def test_real_http_call(self):
        result = self.loop.run_until_complete(core.weather())
        self.assertIn('Температура', result)


class TestYobitRates(unittest.TestCase):
    def setUp(self):
        dictConfig(LOGGING)
        self.loop = asyncio.get_event_loop()

    def test_retrieve_ether_rate(self):
        result = self.loop.run_until_complete(core._retrieve_yobit_rates())
        logger.info('Yobit rates %s', result)
        self.assertIn('eth_usd', result)
        self.assertIn('xem_eth', result)


if __name__ == '__main__':
    unittest.main()
