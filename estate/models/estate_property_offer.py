from odoo import fields, models, api
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError


class EstateOffer(models.Model):
    _name="estate.property.offer"
    _description="A property offer is an amount a potential buyer offers to the seller."
    _sql_constraints = [
        ('check_price', 'CHECK(price > 0)',
         'An offer price must be strictly positive')
    ]
    _order = "price desc"

    price=fields.Float()
    status=fields.Selection(copy=False, selection=[('accepted', 'Accepted'), ('refused', 'Refused')])

    partner_id=fields.Many2one("res.partner", required=True)
    property_id=fields.Many2one("real.estate", required=True)
    property_type_id=fields.Many2one(related="property_id.property_type_id")

    validity = fields.Integer(default=7, string="Validity(days)")
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")
    create_date = fields.Date(default=fields.Date.today())

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = record.create_date + relativedelta(days=record.validity)

    
    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date).days


    def action_accept(self):
        for record in self:
            if "accepted" in record.property_id.offer_ids.mapped("status"):
                raise UserError(" only one offer can be accepted for a given property!")
            else:
                record.status = "accepted"
                record.property_id.buyer_id = record.partner_id
                record.property_id.selling_price = record.price
                record.property_id.state = "accepted"
        return True
    
    def action_refuse(self):
        for record in self:
            record.status = "refused"
        return True
    

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property = self.env['real.estate'].browse(vals['property_id'])
            min_offer=min(property.offer_ids.mapped('price')) if property.offer_ids else 0
            if(vals['price']<min_offer):
                raise UserError("The offer cannot have a lower amount than an existing offer!")
            property.state='received'
        return super().create(vals_list)