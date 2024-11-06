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
from odoo.exceptions import UserError, ValidationError
from odoo.fields import One2many
from odoo.http import request


class RmaOrder(models.Model):
    _name = "rma.order"

    name = fields.Char(string="Name", default=lambda self: 'New')
    order_id = fields.Many2one('sale.order', string="Sale Order", required=True)
    partner_id = fields.Many2one('res.partner', string="Partner", related='order_id.partner_id')
    reason_id = fields.Many2one('rma.reason', string="Reason", required=True)
    reason_type_id = fields.Many2one('rma.stages', string="Reason Type", required=True)
    state = fields.Selection(
        [('new', 'NEW'), ('draft', 'Draft'), ('done', 'Done')], default='new', string="State")
    delivery_count = fields.Integer(string='Delivery Orders',
                                    compute='_compute_delivery_count')
    product_id = One2many('rma.product', 'rma_order_id', string="Product Id")

    @api.onchange('order_id')
    def _onchange_order_id(self):
        if self.order_id:
            self.product_id = [(5, 0, 0)]  # Clear existing products
            product_lines = []
            for line in self.order_id.order_line:
                product_lines.append((0, 0, {
                    'product_id': line.product_id.id,
                    'quantity': line.product_uom_qty,
                    'price': line.price_unit,
                }))
            self.product_id = product_lines  # Assign all the lines at once

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            sale_order_id = vals.get('order_id')

            # Check if an RMA order already exists for the same sale order
            existing_rma = self.search([('order_id', '=', sale_order_id)], limit=1)

            if existing_rma:
                # Get the list of existing product IDs in the existing RMA order
                existing_product_ids = existing_rma.product_id.mapped('product_id.id')

                # Loop through new products in vals['product_id']
                for product in vals.get('product_id', []):
                    if product[0] == 0:  # This means it's a new product being added
                        new_product_id = product[2].get('product_id')
                        new_quantity = product[2].get('quantity', 0)
                        new_price = product[2].get('price', 0)

                        # If the product is already in the existing RMA order, raise an error
                        if new_product_id in existing_product_ids:
                            raise UserError(
                                f"An RMA order for Sale Order '{existing_rma.order_id.name}' "
                                f"and Product '{self.env['product.product'].browse(new_product_id).name}' already exists."
                            )
                        else:
                            # Add a new product to the existing RMA order
                            self.env['rma.product'].create({
                                'rma_order_id': existing_rma.id,
                                'product_id': new_product_id,
                                'quantity': new_quantity,
                                'price': new_price,
                            })

                # Return the existing RMA order without creating a new one
                return existing_rma

            # Generate a sequence number for the 'name' field if it's a new RMA order
            vals['name'] = self.env['ir.sequence'].next_by_code('rma.order') or "New"

        # Create new RMA records if no existing RMA order is found
        records = super(RmaOrder, self).create(vals_list)

        # Set the state to 'draft' after creation
        records.write({'state': 'draft'})

        # Send email for each created record
        customer_template_id = self.env.ref('wbl_return_merchandise_authorization.rma_order_summary')
        admin_template_id = self.env.ref('wbl_return_merchandise_authorization.rma_order_summary_to_admin')

        for record in records:
            # Customer email
            user_email = record.create_uid.partner_id.email  # Get the email of the user who created the record
            print("===user_email======", user_email)

            # Admin email
            admin_email = self.env.ref("base.user_admin").partner_id.email
            print("=====admin_email=", admin_email)

            if user_email:  # Send email to the customer
                customer_email_values = {
                    'email_to': user_email,
                    'email_from': admin_email  # Admin's email as the sender
                }
                customer_template_id.send_mail(record.id, force_send=True, email_values=customer_email_values)

            if admin_email:  # Send email to the admin
                admin_email_values = {
                    'email_to': admin_email,
                    'email_from': user_email  # Admin's email as both sender and receiver
                }
                admin_template_id.send_mail(record.id, force_send=True, email_values=admin_email_values)

        return records

    ####### THIS FUNCTION IS FOR SEND THE EMAIL WHEN THE RMA ORDER WILL BE CONFIRMED #############3
    def write(self, vals):
        if 'state' in vals and vals['state'] == 'done':
            template_id = self.env.ref('wbl_return_merchandise_authorization.rma_order_confirmation')
            for record in self:
                user_id = record.create_uid.partner_id.email  # Assuming you want the creator of the RMA order

                # Use self.env to fetch the email of the admin
                admin_email = self.env.ref("base.user_admin").partner_id.email
                print("=====admin_email=", admin_email)

                if user_id:  # Check if user and email exist
                    email_values = {
                        'email_to': user_id,
                        'email_from': admin_email  # Dynamically pass the admin's email here
                    }
                    template_id.send_mail(record.id, force_send=True, email_values=email_values)
                else:
                    print("Error: User or email not found for record ID:", record.id)

        # Call the parent write method to save the changes
        return super(RmaOrder, self).write(vals)

    @api.depends('order_id')  # It counts the delivery inside the smart button
    def _compute_delivery_count(self):
        print("======_compute_delivery_count===")
        for rma in self:
            pickings = self.env['stock.picking'].search([('origin', '=', rma.name)])
            rma.delivery_count = len(pickings)

    def submit_btn(self):  # By clicking on this button it create the record on table stock picking and stock move
        # Set the state to 'done'
        self.state = 'done'

        # Define source and destination locations manually
        source_location = self.env.ref('stock.stock_location_stock')  # Replace with your actual source location
        destination_location = self.env.ref(
            'stock.stock_location_customers')  # Replace with your actual destination location

        # Ensure you have valid source and destination locations
        if not source_location or not destination_location:
            raise UserError("Please define valid source and destination locations.")

        # Fetch the correct picking type, e.g., delivery order type
        picking_type = self.env.ref('stock.picking_type_out')  # Adjust the external ID to your use case

        if not picking_type:
            raise UserError("Please define a valid picking type.")

        # Create the stock.picking record
        stock_picking_vals = {
            'name': self.env['ir.sequence'].next_by_code('stock.picking') or 'New Picking',  # Assign a name or sequence
            'partner_id': self.partner_id.id,  # The partner to whom the picking is related
            'location_id': source_location.id,  # Source location
            'location_dest_id': destination_location.id,  # Destination location
            'picking_type_id': picking_type.id,  # The picking type (e.g., delivery order)
            'origin': self.name,  # You can reference the RMA order
        }

        # stock picking record
        picking = self.env['stock.picking'].create(stock_picking_vals)

        # Optionally, you can add stock moves here for the products to be transferred
        for product in self.product_id:
            stock_move_vals = {
                'name': product.product_id.name,  # Use the product name
                'product_id': product.product_id.id,  # The product to move
                'product_uom_qty': product.quantity,  # Quantity based on the RMA product
                'product_uom': product.product_id.uom_id.id,  # Unit of measure for the product
                'location_id': source_location.id,  # Source location
                'location_dest_id': destination_location.id,  # Destination location
                'picking_id': picking.id,  # Link the move to the picking
                'state': 'draft',  # Move starts in draft state
            }

            # Create the stock move for each product
            self.env['stock.move'].create(stock_move_vals)

    ########### SMART BUTTON CLICK ON REDIRECT #######################
    def action_view_delivery(self):  # By clicking on this button it redirect you to stock where it is
        self.ensure_one()
        # Search for all stock pickings related to this RMA order
        pickings = self.env['stock.picking'].search([('origin', '=', self.name)])

        if not pickings:
            return {'type': 'ir.actions.act_window_close'}

        # If there is only one picking, open the form view directly
        if len(pickings) == 1:
            action = self.env.ref('stock.action_picking_tree_all').read()[0]
            action['views'] = [(self.env.ref('stock.view_picking_form').id, 'form')]
            action['res_id'] = pickings.id
        else:
            # If there are multiple pickings, open the tree view
            action = self.env.ref('stock.action_picking_tree_all').read()[0]
            action['domain'] = [('id', 'in', pickings.ids)]

        return action
