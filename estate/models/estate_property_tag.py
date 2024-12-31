from odoo import fields, models

class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Tags of Real Estate Model"
    _sql_constraints = [
        ('check_unique_tag_name', 'UNIQUE(name)',
         'Tag name should be unique')
    ]
    _order = "name asc"

    name = fields.Char(required=True)
    color = fields.Integer()

