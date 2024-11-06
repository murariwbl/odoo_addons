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


from odoo import http
from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.http import request


########THIS CONTROLLER IS USED TO SHOW THE RMA DETAIL MAIN VIEW CLICK ON THIS RMA ORDER ID TO SEE THE ALL DETAILS ################
class MyPortalRmaController(http.Controller):
    @http.route('/my/rma/orders', website=True, auth='public')
    def portal_rma(self, **kw):
        current_partner_id = request.env.user.partner_id.id

        # Fetch RMA details for the current user
        rma_details = request.env['rma.order'].sudo().search([('partner_id', '=', current_partner_id)])

        # Prepare the RMA details with state display
        detailed_rma_info = []
        for rma in rma_details:
            state_display = dict(rma.fields_get(allfields=['state'])['state']['selection']).get(rma.state)
            detailed_rma_info.append({
                'id': rma.id,
                'name': rma.name,
                'create_date': rma.create_date,
                'order_id': rma.order_id,
                'reason_type_id': rma.reason_type_id,
                'reason_id': rma.reason_id,
                'state_display': state_display,  # Attach the display state
            })

        values = {
            'rma_details': detailed_rma_info,
            'rma_count': len(rma_details),
        }
        return request.render('wbl_return_merchandise_authorization.wbl_my_portal_rmaorder_view', values)


########## THIS CONTROLLER GIVE THE REASON AND REQUEST TYPE ON PRODUCT RETURN BUTTON  ###############
class RmaReasonController(http.Controller):
    @http.route('/get_rma_reasons', type='json', auth='public', methods=['POST'], website=True, csrf=False)
    def get_rma_reasons(self, order_id=None):
        print("+++++++order_id+++++++++++++", order_id)

        # Use 'name' to find the sale order if 'order_id' is actually a reference
        # sale_order = request.env['sale.order'].search([('name', '=', order_id)], limit=1)
        sale_order = request.env['sale.order'].sudo().search([('name', '=', order_id)], limit=1)

        if not sale_order:
            return {'error': 'Sale order not found'}

        # Find published RMA reasons and request types
        reasons = request.env['rma.reason'].search([('is_published', '=', True)])
        request_type = request.env['rma.stages'].search([('is_published', '=', True)])

        # Prepare the lists to send back to the frontend
        reason_list = [{'id': reason.id, 'name': reason.name} for reason in reasons]
        request_type_list = [{'id': req.id, 'name': req.name} for req in request_type]

        order_lines = []
        for line in sale_order.order_line:
            product_details = {
                'product_id': line.product_id.id,
                'product_name': line.product_id.name,
                'quantity': line.product_uom_qty,
                'price_unit': line.price_unit,
                'subtotal': line.price_subtotal,
            }
            order_lines.append(product_details)

        # Create the response with reasons, request types, and the sale order's product details
        response = {
            'reason_list': reason_list,
            'request_type_list': request_type_list,
            'order_lines': order_lines
        }
        return response


########## THIS CONTROLLER GIVE THE REASON AND REQUEST TYPE ON MAIN RETURN BUTTON  ###############
class RmaReasonTypeController(http.Controller):
    @http.route('/get_rma_reasons_type', type='json', auth='public', methods=['POST'], website=True, csrf=False)
    def get_rma_reasons_type(self, order_id):
        print("+++++++order_id===========", order_id)
        print("xxxxxxxxxxxxxxxxxxxx", order_id)
        reasons = request.env['rma.reason'].search([('is_published', '=', True)])
        request_type = request.env['rma.stages'].search([('is_published', '=', True)])
        reason_list = [{'id': reason.id, 'name': reason.name} for reason in reasons]
        request_type_list = [{'id': req.id, 'name': req.name} for req in request_type]

        # sale_order_id = request.env['sale.order'].search([('id', '=', order_id)])
        sale_order_id = request.env['sale.order'].sudo().search([('name', '=', order_id)], limit=1)
        order_lines = []
        for line in sale_order_id.order_line:
            product_details = {
                'product_id': line.product_id.id,
                'product_name': line.product_id.name,  # Add this field
                'quantity': line.product_uom_qty,
                'price_unit': line.price_unit,
                'subtotal': line.price_subtotal
            }
            order_lines.append(product_details)

        response = {
            'reason_lists': reason_list,
            'request_type_lists': request_type_list,
            'sale_orders': order_lines,  # Ensure you are passing this with product_name
        }
        return response


############ THIS CONTROLLER HIT WHEN WE CLICK ON SUBMIT BUTTON ON PRODUCT PAGE ##########
class SaveRmaReasonController(http.Controller):
    @http.route('/save_rma_reasons', type='json', auth='user')
    def save_rma_reasons(self, order_id, product_id, quantity, reason_type_id, reason_id, price):
        print("====000000000=====", order_id, product_id, quantity, reason_type_id, reason_id, price)

        # Search for an existing RMA order with the same sale order (order_id)
        existing_rma_order = request.env['rma.order'].sudo().search([
            ('order_id', '=', int(order_id)),
        ], limit=1)

        # Check if the product already exists in the RMA order's One2many field (rma.product)
        if existing_rma_order:
            existing_rma_product = request.env['rma.product'].sudo().search([
                ('rma_order_id', '=', existing_rma_order.id),
                ('product_id', '=', int(product_id))
            ], limit=1)

            if existing_rma_product:
                return {
                    'success': False,
                    'message': 'RMA order already exists for this order and product.',
                    'rma_order_id': existing_rma_order.id
                }
            else:
                # Add the new product to the existing RMA order
                request.env['rma.product'].sudo().create({
                    'rma_order_id': existing_rma_order.id,
                    'product_id': int(product_id),
                    'quantity': quantity,  # Assuming quantity is a Char field, handle as needed
                    'price': price  # You can modify this based on your logic for setting price
                })

                return {
                    'success': True,
                    'rma_order_id': existing_rma_order.id
                }
        else:
            # If no existing RMA order is found, create a new RMA order
            rma_order = request.env['rma.order'].sudo().create({
                'order_id': int(order_id),
                'reason_type_id': int(reason_type_id),
                'reason_id': int(reason_id),
                'state': 'draft'
            })

            # Add the product to the newly created RMA order
            request.env['rma.product'].sudo().create({
                'rma_order_id': rma_order.id,
                'product_id': int(product_id),
                'quantity': quantity,  # Assuming quantity is a Char field, handle as needed
                'price': price  # You can modify this based on your logic for setting price
            })

            return {
                'success': True,
                'rma_order_id': rma_order.id
            }


############ THIS CONTROLLER HIT WHEN WE CLICK ON SUBMIT BUTTON ON MAIN PAGE ##########
class SaveRmaOrderReasonController(http.Controller):
    @http.route('/save_rma_order_reasons', type='json', auth='user')
    def save_rma_order_reasons(self, order_id, products, reason_id, reason_type_id):
        print("Received Data:", order_id, products, reason_id, reason_type_id)

        existing_rma_order = request.env['rma.order'].sudo().search([
            ('order_id', '=', int(order_id)),
        ], limit=1)

        if existing_rma_order:
            for product in products:
                existing_rma_product = request.env['rma.product'].sudo().search([
                    ('rma_order_id', '=', existing_rma_order.id),
                    ('product_id', '=', int(product['productId']))  # Access productId instead of product_id
                ], limit=1)

                if existing_rma_product:
                    return {
                        'success': False,
                        'message': f'RMA order already exists for this product.',
                        'rma_order_id': existing_rma_order.id
                    }
                else:
                    request.env['rma.product'].sudo().create({
                        'rma_order_id': existing_rma_order.id,
                        'product_id': int(product['productId']),  # Access productId
                        'quantity': product['quantity'],
                        'price': product['unitPrice']  # Access unitPrice
                    })

            return {
                'success': True,
                'rma_order_id': existing_rma_order.id
            }
        else:
            rma_order = request.env['rma.order'].sudo().create({
                'order_id': int(order_id),
                'reason_type_id': int(reason_type_id),
                'reason_id': int(reason_id),
                'state': 'draft'
            })

            for product in products:
                unit_price = float(product['unitPrice'].replace(',', ''))
                request.env['rma.product'].sudo().create({
                    'rma_order_id': rma_order.id,
                    'product_id': int(product['productId']),  # Access productId
                    'quantity': product['quantity'],
                    'price': unit_price,  # Access unitPrice
                })

            return {
                'success': True,
                'rma_order_id': rma_order.id
            }


#### # # Prepare the RMA details with state display #########
class ReturnCustomerPortal(CustomerPortal):
    """Class for add portal for customer return"""

    def _prepare_home_portal_values(self, counters):
        """To add portal return count"""
        values = super()._prepare_home_portal_values(counters)
        if 'return_count' in counters:
            values['return_count'] = request.env['rma.order'].search_count([
                ('state', 'in', ['new', 'draft', 'submitted'])])
            print("=====values=======", values)
        return values


########## THIS CONTROLLER SHOW THE DETAILS OF RMA ORDER WHILE CLICK ON RMA ORDER ID ###########
class PortalMyRmaOrderDetails(CustomerPortal):
    @http.route(['/rma/return/details/<int:order_id>'], methods=["GET"], type='http',
                auth='public', website=True)
    def portal_my_rma_order_details(self, order_id, **kw):
        print('xxxxxxx', order_id)
        current_partner_id = request.env.user.partner_id.id
        print("==current_partner_id====", current_partner_id)
        rma_order = request.env['rma.order'].sudo().search([('id', '=', order_id)], limit=1)
        print("==rma_order===", rma_order)  # Fetch RMA order by id

        if not rma_order:
            return request.redirect('/my/rma')  # redirect if no RMA found

        detailed_rma_info = [{
            'id': rma_order.id,
            'name': rma_order.name,
            'create_date': rma_order.create_date,
            'order_id': rma_order.order_id,
            'reason_type_id': rma_order.reason_type_id,
            'reason_id': rma_order.reason_id,
            'partner_invoice_id': rma_order.partner_id,
            'partner_shipping_id': rma_order.order_id.partner_shipping_id,
            'order_lines': rma_order.order_id.order_line,
            'state': rma_order.state,
        }]

        values = {
            'rma_det': detailed_rma_info,
            'rma_count': 1,
        }

        return request.render("wbl_return_merchandise_authorization.portal_my_rma_order_details", values)
