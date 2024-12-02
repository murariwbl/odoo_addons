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
import re


class PortalMyProductDetailsPdf(http.Controller):

    #########   THIS CONTROLLER HIT WHEN WE CLICK ON VIEW BUTTON INSIDE THE SHIPPING QUOTATION LIST ##############
    @http.route(['/shipping/quotation/download'], type='http', auth='public', website=True)
    def portal_my_product_details_pdf(self, **kw):
        # Get the quotation_id from the URL parameters
        quotation_id = kw.get('quotation_id')

        # Fetch the quotation record from the database using the quotation ID
        quotation = request.env['carrier.quotation'].sudo().search([('name', '=', quotation_id)], limit=1)

        # Check if a sale order exists with this quotation_id
        sale_order = request.env['sale.order'].sudo().search([('quotation_id', '=', quotation.id)], limit=1)
        sale_order_exists = bool(sale_order)

        # Check if order and currency_id exist
        currency_symbol = quotation.currency_id.symbol

        # Prepare product details
        product_lines = []

        for product_line in quotation.product_ids:
            # Ensure Total is a string
            line_total = str(product_line.Total or '0')

            # Clean line_total using regex to remove currency symbols and commas
            try:
                # Remove known currency symbol
                if currency_symbol:
                    line_total = line_total.replace(currency_symbol, '')

                line_total = re.sub(r'[^\d.]+', '', line_total)
                print("Cleaned line_total:", line_total)

                # Convert to float
                line_total = float(line_total or 0.0)
            except ValueError:
                # Fallback to 0.0 if conversion fails
                print(f"Invalid line_total format: {product_line.Total}")
                line_total = 0.0

        # Fetch the product image
        product_image = product_line.product_id.image_128

        # Append cleaned data to product lines
        product_lines.append({
            'product_id': product_line.product_id.id,
            'product_name': product_line.product_id.name,
            'unit_price': product_line.unit_price,
            'product_quantity': product_line.product_quantity,
            'total': line_total,
            'image_128': product_image,
        })

        # Access partner details
        partner_name = request.env.user.partner_id.name
        partner_address = request.env.user.partner_id.contact_address  # Assuming 'contact_address' is a field
        partner_phone = request.env.user.partner_id.phone
        partner_email = request.env.user.partner_id.email

        # Calculate subtotal
        total_products_amount = sum(float(line['total']) for line in product_lines)
        shipping_price = float(quotation.shipping_price or 0.0)
        subtotal = total_products_amount + shipping_price

        values = {
            'quotation': quotation,
            'customer_name': quotation.customer_name,
            'customer_email': quotation.customer_email,
            'carrier': quotation.carrier,
            'Received_date': quotation.Received_date,
            'expired_date': quotation.expired_date,
            'message': quotation.message,
            'status': quotation.status,
            'partner_name': partner_name,
            'partner_address': partner_address,
            'partner_phone': partner_phone,
            'partner_email': partner_email,
            'total': quotation.total,
            'shipping_price': quotation.shipping_price,
            'product_lines': product_lines,  # Add product lines to the context
            'subtotal': subtotal,
            'total_products_amount': total_products_amount,
            'currency_symbol': currency_symbol,
            'sale_order_exists': sale_order_exists,  # Pass the existence flag
        }
        # Render the PDF
        report_service = request.env['ir.actions.report']
        pdf_content, _ = report_service._render_qweb_pdf(
            'wbl_shipping_quotation.action_report_shipping_quotation_pdf', [], values
        )

        # Create a response to download the PDF
        response = request.make_response(pdf_content, headers=[
            ('Content-Type', 'application/pdf'),
            ('Content-Disposition', f'attachment; filename="{quotation.name}_quotation_details.pdf"'),

        ])

        return response
