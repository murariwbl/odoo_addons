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
from odoo.http import request
from datetime import datetime, timedelta
import uuid  # To generate a unique identifier


class CarrierQuotationController(http.Controller):

    ##########  THIS CONTROLLER HIT WHEN WE CLICK THE QUOTATION RAISE BUTTON ON SELECT SHIPPING METHOD ############
    @http.route('/custom/save_carrier_quotation', type='json', auth='public', website=True, methods=['POST'])
    def save_carrier_quotation(self, text_message=None):
        # Get the current sale order
        order = request.website.sale_get_order()
        if not order:
            return {'error': 'No active sale order found'}

        total_with_currency_symbol = f"{order.currency_id.symbol}{order.amount_total:.2f}"
        current_date = datetime.today().strftime('%Y-%m-%d')

        # Get the shipping price
        shipping_line = order.order_line.filtered(lambda line: line.is_delivery)
        if shipping_line:
            delivery_charge = shipping_line.price_unit  # Use numeric value
        elif order.carrier_id and order.carrier_id.fixed_price:
            delivery_charge = order.carrier_id.fixed_price  # Use numeric value
        else:
            delivery_charge = 0.0  # Default to zero if no shipping price is available

        # Calculate the expiration date using the `quote_expire` field from the delivery carrier
        if order.carrier_id and order.carrier_id.quote_expire:
            expire_days = order.carrier_id.quote_expire
            expire_date = (datetime.today() + timedelta(days=expire_days)).strftime('%Y-%m-%d')
        else:
            expire_date = current_date  # Default to the current date if no expiration days are specified

        # Generate a unique quotation ID using UUID
        unique_quotation_id = request.env['ir.sequence'].sudo().next_by_code('carrier.quotation')
        # unique_quotation_id = f"QUE-{uuid.uuid4().hex[:4]}"  # Generate a unique 4-character string with the prefix 'QUE-'

        # Check if a quotation with the same unique_quotation_id already exists
        existing_quotation = request.env['carrier.quotation'].sudo().search([('name', '=', unique_quotation_id)],
                                                                            limit=1)
        if existing_quotation:
            return {'success': False, 'error': 'Quotation already exists'}

        # Prepare the data to create a Carrier Quotation record
        quotation_data = {
            'name': unique_quotation_id,  # Use the unique quotation ID
            'cart_id': str(order.id),
            'customer_name': order.partner_id.name,
            'customer_email': order.partner_id.email,
            'total': order.amount_total,
            'carrier': order.carrier_id.name if order.carrier_id else 'N/A',
            'shipping_price': delivery_charge,
            'Received_date': current_date,
            'expired_date': expire_date,  # Use the calculated expiration date
            'carrier_id': order.carrier_id.id,
            'message': text_message,  # Save the text message

        }

        # Create the Carrier Quotation record
        quotation = request.env['carrier.quotation'].sudo().create(quotation_data)

        # Add products to the QuotationProduct model, linked to the created carrier.quotation
        product_lines = []
        for line in order.order_line:
            if not line.is_delivery:  # Exclude delivery lines
                unit_price_with_symbol = f"{order.currency_id.symbol}{line.price_unit:.2f}"
                total_with_symbol = f"{order.currency_id.symbol}{line.price_subtotal:.2f}"

                product_lines.append((0, 0, {
                    'product_id': line.product_id.id,
                    'quotation_id': quotation.id,
                    'unit_price': unit_price_with_symbol,  # Unit price with currency symbol
                    'product_quantity': line.product_uom_qty,  # Quantity of the product
                    'Total': total_with_symbol,  # Total with currency symbol
                }))

        # Write product lines to the quotation record
        if product_lines:
            quotation.write({'product_ids': product_lines})

        # Clear the cart after the quotation is created
        if order:
            order._clear_cart()  # Remove all order lines

        # Return success response
        return {
            'success': True,
            'quotation_id': quotation.id,
            'message': "Quotation created successfully, and cart cleared."
        }
