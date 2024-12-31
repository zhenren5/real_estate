from odoo import fields, models, api



class EstateAccount(models.Model):
    _name="estate.account"
    _description="depends on estate and account and would include the invoice creation logic of the estate property."
    