
from odoo import models, fields


class res_users(models.Model):
    _inherit = 'res.users'

    property_ids = fields.One2many("real.estate","salesperson_id")