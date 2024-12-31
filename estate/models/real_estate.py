from odoo import _,api, fields, models
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare

class RealEstate(models.Model):
    _name = "real.estate"
    _description = "Tutorial description"
    _sql_constraints = [
        ('check_selling_price', 'CHECK(selling_price >= 0 )',
         'A property selling price must be positive'),
        ('check_expected_price', 'CHECK(expected_price > 0 )',
         'A property expected price must be strictly positive') 
    ]
    _order = "id desc"

    name = fields.Char(default="House", required=True, string="Title")
    description = fields.Text()
    postcode = fields.Char(string="Postcode")
    active = fields.Boolean(default=True)

    def _default_date(self):
        return fields.Date.today() + relativedelta(months=3)
    date_availability = fields.Date(default=_default_date, string="Available From")
    expected_price = fields.Float(copy=False, string="Expected Price")
    selling_price = fields.Float(copy=False, readonly=True, string="Selling Price")
    bedrooms = fields.Integer(default=2, string="Bedrooms")
    living_area = fields.Integer(string="Living Area(sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
    )
    
    state = fields.Selection(
        selection=[('new',"New"), ('received',"Offer Received"),('accepted',' Offer Accepted'), ('sold', 'Sold'), ('cancelled','Cancelled')],
        default='new',
        required=True,
        copy=False
    )   

    property_type_id = fields.Many2one("property.type")
    buyer_id = fields.Many2one("res.partner",string="Buyer" , copy=False)
    salesperson_id = fields.Many2one("res.users", string='Salesperson', default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id")
    total_area = fields.Integer(compute="_compute_total_area", string="Total Area(sqm)")
    best_price = fields.Float(compute="_compute_best_offer", string="Best Offer")


    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_offer(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price')) if record.offer_ids else 0


    # @api.depends("offer_ids.status")
    # def _compute_best_offer(self):
    #     for record in self:
    #         record.status = 'accepted' if record.offer_ids.status.mapped('status') in ["accepted"] else 'received'



    @api.onchange("garden")
    def _onchange_garden(self):
        for record in self:
            if record.garden:
                self.garden_area = 10
                self.garden_orientation = "north"
            else:
                self.garden_area = 0
                self.garden_orientation = False

    def action_sold(self):
        for record in self:
            if record.state == "cancelled":
                raise UserError(" A cancelled property cannot be set as sold.")
            else:
                record.state = "sold"
        
    def action_cancel(self):
        for record in self:
            if record.state == "sold":
                raise UserError(" A sold property cannot be cancelled.")
            else:
                record.state = "cancelled"

    @api.constrains('selling_price')
    def _check_selling_price(self):
        for record in self:
            if float_compare(record.selling_price, record.expected_price*0.9, precision_digits=2) < 0:
                raise ValidationError(
                    "The selling price cannot be lower than 90% of the expected price. "
                    f"(Selling Price: {record.selling_price}, Expected Price: {record.expected_price})"
                )
            
    @api.ondelete(at_uninstall=False)
    def _prevent_deletion_if_not_new_or_cancelled(self):
        for record in self:
            if record.state not in ['new', 'cancelled']:
                raise UserError(_(
                    "You cannot delete the property if its state is not 'New' or 'Cancelled'."
                ))
            
 