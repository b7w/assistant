import unittest
from decimal import Decimal
from logging.config import dictConfig

from assistant.tests import LOGGING
from assistant.utils import parse_money


class TestMoneyParse(unittest.TestCase):
    def setUp(self):
        dictConfig(LOGGING)

    def _assert(self, text, amount, currency):
        self.assertEqual((Decimal(amount), currency), parse_money(text), text)

    def test_parse_usd(self):
        self._assert('$10', '10', 'USD')
        self._assert('10$', '10', 'USD')
        self._assert('$ 10', '10', 'USD')
        self._assert('10 $', '10', 'USD')
        self._assert('10 Usd', '10', 'USD')
        self._assert('12 34 $', '12', 'USD')
        self._assert('12,34 $', '12.34', 'USD')
        self._assert('12.34 $', '12.34', 'USD')

    def test_parse_eur(self):
        self._assert('€10', '10', 'EUR')
        self._assert('10€', '10', 'EUR')
        self._assert('€ 10', '10', 'EUR')
        self._assert('10 €', '10', 'EUR')
        self._assert('10 eUr', '10', 'EUR')
        self._assert('12 34 €', '12', 'EUR')
        self._assert('12.34 €', '12.34', 'EUR')
        self._assert('12,34 €', '12.34', 'EUR')

    def test_parse_all(self):
        self._assert('10', '10', None)
        self._assert('1 2 3', '1', None)


if __name__ == '__main__':
    unittest.main()
