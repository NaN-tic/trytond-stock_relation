# This file is part of the stock_relation module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import unittest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase


class StockRelationTestCase(ModuleTestCase):
    'Test Stock Relation module'
    module = 'stock_relation'


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        StockRelationTestCase))
    return suite
