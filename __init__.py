# This file is part of the stock_relation module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
from . import move


def register():
    Pool.register(
        move.OpenMovesStart,
        module='stock_relation', type_='model')
    Pool.register(
        move.OpenMoves,
        module='stock_relation', type_='wizard')
