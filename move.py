# This file is part of the stock_relation module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from datetime import date
from trytond.model import ModelView, fields
from trytond.pyson import PYSONEncoder
from trytond.transaction import Transaction
from trytond.wizard import Button, StateAction, StateView, Wizard

__all__ = ['OpenMovesStart', 'OpenMoves']


class OpenMovesStart(ModelView):
    'Open Moves'
    __name__ = 'stock.location.open_moves.start'
    effective_date = fields.Date(
        'At Date', help=('Allow to compute expected '
            'stock quantities for this date.\n'
            '* An empty value is an infinite date in the future.\n'
            '* A date in the past will provide historical values.'))
    product = fields.Many2One('product.product', 'Product')

    @staticmethod
    def default_effective_date():
        return date.today()


class OpenMoves(Wizard):
    'Open Moves'
    __name__ = 'stock.location.open_moves'
    start = StateView('stock.location.open_moves.start',
        'stock_relation.stock_location_open_moves_start', [
            Button('Cancel', 'end', 'tryton-cancel'),
            Button('Open', 'open_', 'tryton-ok', default=True),
            ])
    open_ = StateAction('stock_relation.act_moves_for_location')

    def do_open_(self, action):
        context = Transaction().context
        location_id = context['active_id']
        context['location'] = location_id
        if self.start.effective_date:
            context['effective_date'] = self.start.effective_date
        else:
            context['effective_date'] = date.max
        if 'product' not in context and self.start.product:
            context['product'] = self.start.product.id
        action['pyson_context'] = PYSONEncoder().encode(context)

        action['pyson_domain'] = [
            ['OR',
                ('from_location', '=', location_id),
                ('to_location', '=', location_id)
                ],
            ('effective_date', '<=', context['effective_date']),
            ]
        if 'product' in context:
            action['pyson_domain'].append(('product', '=', context['product']))
        action['pyson_domain'] = PYSONEncoder().encode(action['pyson_domain'])
        return action, {}
