from odoo import api, fields, models


class DeliveryCarrier(models.Model):
    _inherit = 'delivery.carrier'

    enable_quotation = fields.Boolean(String="Enable Quotation")
    require_message_box = fields.Boolean(String="Require Message Text Box")
    button_name = fields.Char(String="Button Name")
    message_show = fields.Boolean(String="Show Message Text Box")
    custom_message = fields.Text(String="Custom Message")
    quote_expire = fields.Integer(string="Quote Expire After (days)",
                                  help="Number of days after which the quote expires")


