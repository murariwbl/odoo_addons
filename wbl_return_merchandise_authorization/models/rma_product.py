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


class RmaProduct(models.Model):
    _name = "rma.product"

    rma_order_id = fields.Many2one('rma.order')
    product_id = fields.Many2one('product.product', string="Product")
    quantity = fields.Float(string="Quantity")
    price = fields.Float(string="Price")
