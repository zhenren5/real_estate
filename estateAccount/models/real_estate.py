from odoo import models, Command

class RealEstate(models.Model):
    _inherit = "real.estate"

    def action_sold(self):
        for record in self:
            moves = self.env['account.move'].create({
            'partner_id': record.buyer_id.id,  # Partner linked to the property
            'move_type': 'out_invoice',           # Customer Invoice
            "name": "Test",
            'invoice_line_ids': [
                Command.create({
                    'name': 'Selling Price Commission (6%)',
                        'quantity': 1,
                        'price_unit': record.selling_price * 0.06,
                }),
                Command.create({
                    'name': 'Administrative Fees',
                        'quantity': 1,
                        'price_unit': 100.00,
                }),
    
                ],
        })
        return super().action_sold()