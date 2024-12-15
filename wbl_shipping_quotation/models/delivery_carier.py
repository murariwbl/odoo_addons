# -*- coding: utf-8 -*-
#
#################################################################################
# Author      : Weblytic Labs Pvt. Ltd. (<https://store.weblyticlabs.com/>)
# Copyright(c): 2023-Present Weblytic Labs Pvt. Ltd.
# All Rights Reserved.
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
##################################################################################


from odoo import api, fields, models
import logging

_logger = logging.getLogger(__name__)


class DeliveryCarrier(models.Model):
    _inherit = 'delivery.carrier'

    enable_quotation = fields.Boolean(String="Enable Quotation")
    require_message_box = fields.Boolean(String="Require Message Text Box")
    button_name = fields.Char(String="Button Name")
    message_show = fields.Boolean(String="Show Message Text Box")
    custom_message = fields.Html(String="Custom Message")
    quote_expire = fields.Integer(string="Quote Expire After (days)",
                                  help="Number of days after which the quote expires")
    currency_id = fields.Many2one('res.currency', required=True,
                                  default=lambda self: self.env.company.currency_id)
    minimum_order_amount = fields.Float(string="Minimum Order Amount")
    is_tax_include = fields.Boolean(string="Tax Exclude")
    product_ids = fields.Many2many('product.product', String="Products")
    date_from = fields.Date(String="From")
    date_to = fields.Date(String="To")
    customer_ids = fields.Many2many('res.partner', string="Customers")
    select_country = fields.Many2many('res.country', string="Country")

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
