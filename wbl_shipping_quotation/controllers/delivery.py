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
from datetime import datetime


class DeliveryCarrierController(http.Controller):
    ######## THIS CONTROLLER HIT WHEN WE SELECT THE SHIPPING METHOD ###################
    @http.route('/custom/get_delivery_carrier', type='json', auth='public', methods=['POST'])
    def get_delivery_carrier(self, dm_id=None):
        if not dm_id:
            return {'error': 'dm_id is required'}

        carrier = request.env['delivery.carrier'].sudo().search([('id', '=', dm_id)], limit=1)
        if not carrier:
            return {'error': 'Carrier not found'}

        # Ensure we are accessing the website correctly
        website = request.env['website'].sudo().get_current_website()
        if not website:
            return {'error': 'Website not found'}

        order = website.sale_get_order(force_create=True)

        sale_order = request.env['sale.order'].sudo().search([('id', '=', request.session.get('sale_order_id'))],
                                                             limit=1)
        if not sale_order:
            return {'error': 'No active sale order'}

        # Initialize conditions_matched variable
        conditions_matched = True

        # Minimum Order Filter
        if carrier.minimum_order_amount:
            minimum_order_amount = carrier.minimum_order_amount or 0.0
            tax_excluded = carrier.is_tax_include or False

            if minimum_order_amount > 0:  # Only perform checks if minimum_order_amount is positive
                if tax_excluded:
                    min_order_match = order.amount_untaxed >= minimum_order_amount
                else:
                    min_order_match = order.amount_total >= minimum_order_amount
            else:
                min_order_match = False

            if not min_order_match:
                conditions_matched = False
        else:
            print("Minimum Order Filter not applied as 'apply_minimum_order_filter' is disabled.")

        # Product Filter
        if carrier.product_ids:
            product_ids = carrier.product_ids
            order_product_ids = sale_order.order_line.mapped('product_id.id')
            product_match = any(product_id.id in order_product_ids for product_id in product_ids)

            if not product_match:
                conditions_matched = False
        else:
            print("product selection is disable")

            # Customer Filter
        if carrier.customer_ids:
            customer_match = carrier.customer_ids.filtered(lambda c: c.id == sale_order.partner_id.id)
            has_customer_match = bool(customer_match)

            if not has_customer_match:
                conditions_matched = False
        else:
            print("carrier selection  is disable.")

        # Country Filter
        if carrier.select_country:
            country_match = carrier.select_country.filtered(lambda c: c.id == sale_order.partner_id.country_id.id)
            has_country_match = bool(country_match)

            if not has_country_match:
                conditions_matched = False
        else:
            print("=======select country is disable")

        # Calendar Filter
        if carrier.date_from and carrier.date_to:
            date_match = False
            from_date = carrier.date_from or None
            to_date = carrier.date_to or None
            current_date = datetime.now().date()
            if from_date and to_date:
                date_match = from_date <= current_date <= to_date

            if not date_match:
                conditions_matched = False
        else:
            print("=====date from and date to is disable")

        # Prepare the result dictionary
        result = {
            'enable_quotation': carrier.enable_quotation,
            'message_show': carrier.message_show,
            'custom_message': carrier.custom_message,
            'button_name': carrier.button_name,
            'shipping_quotation': sale_order.shipping_quotation,
            'conditions_matched': conditions_matched  # Add the new flag
        }

        if conditions_matched:
            return result

        return {
            'error': 'Carrier does not match any filters',
            'show_button': False,  # Explicitly hide the button in error cases
            'conditions_matched': conditions_matched  # Include the flag in error case as well
        }
