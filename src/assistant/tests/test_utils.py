import logging
import unittest
from datetime import timedelta, date, datetime, time
from logging.config import dictConfig

from assistant.tests import LOGGING
from assistant.utils import cycle_day_left

logger = logging.getLogger(__name__)


class TestIsCycleDay(unittest.TestCase):
    def setUp(self):
        dictConfig(LOGGING)
        self.start = date.fromisoformat('2019-01-01')

    def _shift_start_date(self, days):
        return datetime.combine(self.start, time.min) + timedelta(days=days)

    def test_day(self):
        self.assertEqual(cycle_day_left(self.start, self._shift_start_date(0)), 0)
        self.assertEqual(cycle_day_left(self.start, self._shift_start_date(1)), 3)
        self.assertEqual(cycle_day_left(self.start, self._shift_start_date(2)), 2)
        self.assertEqual(cycle_day_left(self.start, self._shift_start_date(3)), 1)
        self.assertEqual(cycle_day_left(self.start, self._shift_start_date(4)), 0)
        self.assertEqual(cycle_day_left(self.start, self._shift_start_date(5)), 3)

    def test_day_shift(self):
        self.assertEqual(cycle_day_left(self.start, self._shift_start_date(0), shift=1), 1)
        self.assertEqual(cycle_day_left(self.start, self._shift_start_date(1), shift=1), 0)
        self.assertEqual(cycle_day_left(self.start, self._shift_start_date(2), shift=1), 3)


if __name__ == '__main__':
    unittest.main()
