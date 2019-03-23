import logging
import unittest
from datetime import timedelta, date, datetime, time
from logging.config import dictConfig

from assistant.tests import LOGGING
from assistant.utils import is_cycle_day

logger = logging.getLogger(__name__)


class TestIsCycleDay(unittest.TestCase):
    def setUp(self):
        dictConfig(LOGGING)
        self.start = date.fromisoformat('2019-01-01')

    def _shift_start_date(self, days):
        return datetime.combine(self.start, time.min) + timedelta(days=days)

    def test_day(self):
        self.assertTrue(is_cycle_day(self.start, self._shift_start_date(0)))
        self.assertFalse(is_cycle_day(self.start, self._shift_start_date(1)))
        self.assertFalse(is_cycle_day(self.start, self._shift_start_date(2)))
        self.assertFalse(is_cycle_day(self.start, self._shift_start_date(3)))
        self.assertTrue(is_cycle_day(self.start, self._shift_start_date(4)))

    def test_day_with_shift(self):
        self.assertTrue(is_cycle_day(self.start, self._shift_start_date(5), shift=1))
        self.assertTrue(is_cycle_day(self.start, self._shift_start_date(9), shift=1))


if __name__ == '__main__':
    unittest.main()
