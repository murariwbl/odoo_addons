from odoo import api, fields, models
from datetime import date, datetime, time
import logging

_logger = logging.getLogger(__name__)


class CarrierQuotation(models.Model):
    _name = "carrier.quotation"

    name = fields.Char(string="Quotation Id")
    cart_id = fields.Char(string="Cart Id")
    status = fields.Selection(
        [('open', 'Open'), ('sent', 'Sent')], default='open', string="status")
    customer_name = fields.Char(string="Customer Name")
    customer_email = fields.Char(string="Customer Email")
    total = fields.Float(string="Total")
    carrier = fields.Char(string="Carrier")
    currency_id = fields.Many2one('res.currency', string='Currency', required=True,
                                  default=lambda self: self.env.company.currency_id)
    shipping_price = fields.Float(string="Shipping Price")
    Received_date = fields.Date(string="Received Date")
    expired_date = fields.Date(string="Expired Date")
    message = fields.Char(string="Message")
    product_ids = fields.One2many('quotation.product', 'quotation_id', string="Products")
    carrier_id = fields.Many2one('delivery.carrier', string="Carrier Id")

    ########For changing the state ##########
    def approve_action(self):
        for record in self:
            record.status = 'sent'
        return True

    #####  THIS IS CRON I HAVE USED THIS TO DELETE THE RECORD WHEN THE EXPIRATION DATE WILL PASS  #########
    @api.model
    def delete_expired_quotations(self):
        print("ir cron function triggerd")
        """Deletes quotations whose expired_date has passed."""
        today = datetime.today().date()  # Get today's date
        expired_quotations = self.search([('expired_date', '<', today)])

        if expired_quotations:
            # Log the expired quotations
            _logger.info(f"Deleting {len(expired_quotations)} expired quotations.")
            # Delete expired quotations
            expired_quotations.unlink()
        else:
            _logger.info("No expired quotations found.")
