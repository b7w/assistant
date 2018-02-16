import unittest
from logging.config import dictConfig

from assistant.core import parse_money
from assistant.tests import LOGGING


class TestMoneyParse(unittest.TestCase):
    def setUp(self):
        dictConfig(LOGGING)

    def _assert(self, text, amount, currency):
        self.assertEqual((amount, currency), parse_money(text))

    def test_parse_usd(self):
        self._assert('$10', 10, 'USD')
        self._assert('10$', 10, 'USD')
        self._assert('$ 10', 10, 'USD')
        self._assert('10 $', 10, 'USD')
        self._assert('10 Usd', 10, 'USD')
        self._assert('12 34 $', 1234, 'USD')
        self._assert('12,34 $', 1234, 'USD')
        self._assert('12.34 $', 1234, 'USD')

    def test_parse_eur(self):
        self._assert('€10', 10, 'EUR')
        self._assert('10€', 10, 'EUR')
        self._assert('€ 10', 10, 'EUR')
        self._assert('10 €', 10, 'EUR')
        self._assert('10 eUr', 10, 'EUR')
        self._assert('12 34 €', 1234, 'EUR')
        self._assert('12.34 €', 1234, 'EUR')
        self._assert('12,34 €', 1234, 'EUR')

    def test_parse_all(self):
        self._assert('10', 10, None)
        self._assert('1 2 3', 123, None)


if __name__ == '__main__':
    unittest.main()
