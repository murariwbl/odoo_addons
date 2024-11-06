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


from odoo import _, api, fields, models
from odoo.exceptions import UserError


class RmaOrderWizard(models.TransientModel):
    _name = 'rma.order.wizard'

    sale_order_id = fields.Many2one('sale.order', string="Order ID", readonly=True)
    order_line_ids = fields.Many2many('sale.order.line', domain="[('order_id', '=', sale_order_id)]")
    reason_id = fields.Many2one('rma.reason', string="Reason", required=True)
    reason_type_id = fields.Many2one('rma.stages', string="Reason Type", required=True)

    @api.model
    def default_get(self, fields):
        res = super(RmaOrderWizard, self).default_get(fields)
        sale_order_id = self.env.context.get('active_id')
        if sale_order_id:
            sale_order = self.env['sale.order'].browse(sale_order_id)
            res.update({
                'sale_order_id': sale_order.id,
                'order_line_ids': [(6, 0, sale_order.order_line.ids)]
            })
        return res

    def action_create_rma_wizard(self):
        print("======Hello brother====")
        sale_order = self.sale_order_id  # Get the sale order associated with this wizard
        reason_type = self.reason_type_id.id
        reason = self.reason_id.id
        print("=====sale_order=====", sale_order, sale_order.partner_id.name)

        # Iterate over the sale order lines to check for existing RMA products
        for line in self.order_line_ids:
            print(f"Product: {line.product_id.name}, Quantity: {line.product_uom_qty}, Price: {line.price_unit}")

            # Check if an RMA product already exists for the same sale order and product
            existing_rma_product = self.env['rma.product'].sudo().search([
                ('rma_order_id.order_id', '=', sale_order.id),  # Match with Sale Order ID through RMA order
                ('product_id', '=', line.product_id.id)  # Match with Product ID
            ], limit=1)

            # If an RMA product already exists, raise a UserError and stop the process
            if existing_rma_product:
                raise UserError(
                    f"The RMA for product '{line.product_id.name}' in sale order '{sale_order.name}' already exists."
                )

        # If no existing RMA product is found, create a new RMA order
        rma_order = self.env['rma.order'].sudo().create({
            'order_id': sale_order.id,  # Directly use sale_order.id
            'reason_type_id': reason_type,
            'reason_id': reason,
            'state': 'draft'
        })

        # Create new RMA product lines after confirming no duplicates exist
        for line in self.order_line_ids:
            self.env['rma.product'].sudo().create({
                'rma_order_id': rma_order.id,  # Link to the newly created RMA order
                'product_id': line.product_id.id,
                'quantity': line.product_uom_qty,
                'price': line.price_unit
            })

        return {
            'success': True,
            'rma_order_id': rma_order.id,
            'effect': {
                'fadeout': 'slow',  # Slow fade-out effect
                'message': f'RMA Order {rma_order.name} has been created successfully!',
                'type': 'rainbow_man',  # Rainbow effect
            }
        }
