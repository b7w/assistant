import asyncio
import logging
import unittest
from datetime import datetime, timedelta
from logging.config import dictConfig

from assistant import core
from assistant.tests import LOGGING

logger = logging.getLogger(__name__)


class TestWeather(unittest.TestCase):
    def setUp(self):
        dictConfig(LOGGING)
        self.loop = asyncio.get_event_loop()

    def test_real_http_call(self):
        result = self.loop.run_until_complete(core.yandex_weather())
        self.assertIn('Температура', result)


@unittest.skip('Need to setup env.SOCKS5_PROXY_URL')
class TestYobitRates(unittest.TestCase):
    def setUp(self):
        dictConfig(LOGGING)
        self.loop = asyncio.get_event_loop()

    def test_retrieve_ether_rate(self):
        result = self.loop.run_until_complete(core._retrieve_yobit_rates())
        logger.info('Yobit rates %s', result)
        self.assertIn('eth_usd', result)
        self.assertIn('xem_eth', result)


class TestWorkDay(unittest.TestCase):
    def setUp(self):
        dictConfig(LOGGING)
        self.first_work_day = datetime.now().date()

    def _assert(self, days, text):
        work_day = datetime.now() + timedelta(days=days)
        result = core._workday(self.first_work_day, work_day)
        self.assertEqual(text, result)

    def test_workday(self):
        self._assert(0, 'Сегодня рабочий день')
        self._assert(1, 'Сегодня отсыпной день')
        self._assert(2, 'Осталось 2 дня до рабочего дня')
        self._assert(3, 'Завтра рабочий день')
        self._assert(4, 'Сегодня рабочий день')


class TestSechenovAppointment(unittest.TestCase):
    def setUp(self):
        dictConfig(LOGGING)
        self.loop = asyncio.get_event_loop()

    def test(self):
        result = self.loop.run_until_complete(core.sechenov_find_tickets('Д'))
        self.assertIsNotNone(result)


if __name__ == '__main__':
    unittest.main()
