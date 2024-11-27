from odoo import api, fields, models
import logging

_logger = logging.getLogger(__name__)


class DeliveryCarrier(models.Model):
    _inherit = 'delivery.carrier'

    enable_quotation = fields.Boolean(String="Enable Quotation")
    require_message_box = fields.Boolean(String="Require Message Text Box")
    button_name = fields.Char(String="Button Name")
    message_show = fields.Boolean(String="Show Message Text Box")
    custom_message = fields.Text(String="Custom Message")
    quote_expire = fields.Integer(string="Quote Expire After (days)",
                                  help="Number of days after which the quote expires")

    def rate_shipment(self, order):
        # Call the super method to get the default response
        response = super(DeliveryCarrier, self).rate_shipment(order=order)

        # Ensure the order and the necessary fields exist
        if order and order.quotation_id and order.quotation_id.carrier_id:
            # Match the carrier ID
            if order.quotation_id.carrier_id == self:
                # Update the shipping price
                shipping_price = order.quotation_id.shipping_price
                response['price'] = shipping_price

                # Optionally, you can log or debug the updated price
                _logger.info(f"Updated shipping price for carrier {self.name}: {shipping_price}")

        return response
