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


class QuotationProduct(models.Model):
    _name = "quotation.product"

    quotation_id = fields.Many2one('carrier.quotation', string="Quotation Reference")
    product_id = fields.Many2one('product.product', string="Product")
    unit_price = fields.Char(string="Unit Price")
    product_quantity = fields.Char(string="Quantity")
    Total = fields.Char(String="Total")
