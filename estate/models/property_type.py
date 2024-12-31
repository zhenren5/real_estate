from odoo import fields, models,api

class PropertyType(models.Model):
    _name = "property.type"
    _description = "A property type is, for example, a house or an apartment."
    _sql_constraints = [
        ('check_unique_type_name', 'UNIQUE(name)',
         'Type name should be unique')
    ]
    _order = "sequence desc, name asc"

    sequence = fields.Integer(default=1)
    name = fields.Char(string="Name", required=True)
    property_ids = fields.One2many("real.estate","property_type_id")
    offer_ids = fields.One2many("estate.property.offer","property_type_id")
    offer_count = fields.Integer(compute="_compute_offer_count")

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count=len(record.offer_ids)

    # def action_display_offers(self):
    #     return {
    #         "name": ("Property Offers"),
    #         "type": "ir.actions.act_window",
    #         "view_mode": "list,form",
    #         "res_model": "estate.property.offer",
    #         "target": "current",
    #         "domain": [("property_type_id", "=", self.id)],
    #         "context": {"default_property_type_id": self.id}
    #     }
    

