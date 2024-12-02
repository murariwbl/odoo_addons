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


##############  THIS CONTROLLER WORK WHEN WE CLICK ON  PDF BUTTON INSIDE THE PRODUCT PAGE AND IT DOWNLOAD THE PDF  #############
class PortalMyAllProductDetailsPdf(http.Controller):
    @http.route(['/all/product/pdf'], methods=["GET"], auth='public', website=True)
    def portal_my_all_product_details_pdf(self, **kw):
        print("=====button clicked Inside The product PDF download=====")
        settings = request.env['res.config.settings'].sudo().get_values()
        # print("====settings===", settings)

        # Extract category_ids as a list of integers
        # Extract category_ids as a list of integers
        setting_product_category_ids_command = settings.get("category_ids")
        allowed_category_ids = setting_product_category_ids_command[0][
            2] if setting_product_category_ids_command else []

        # Fetch all published products if no categories are set, otherwise filter by category
        product_domain = [('website_published', '=', True)]
        if allowed_category_ids:
            product_domain.append(('categ_id', 'in', allowed_category_ids))

        products = request.env['product.template'].sudo().search(product_domain)
        print("======", products)

        # Prepare values for the template
        products_data = []
        for product in products:
            # print("===",product.image_128)
            # Collect attributes for each product
            attributes = []
            for attribute_line in product.attribute_line_ids:
                for value in attribute_line.value_ids:
                    attributes.append({
                        'attribute': attribute_line.attribute_id.name,
                        'value': value.name,
                    })

            products_data.append({
                'name': product.name,
                'description': product.description_ecommerce or '',
                # 'description': product.description_sale or '',
                'image': product.image_1920.decode('utf-8') if product.image_1920 else None,
                'price': f"{product.list_price:.2f}",
                'currency_symbol': product.currency_id.symbol or '',
                'attributes': attributes,
            })

            # print("======products_data", products_data)

        current_date = datetime.today().strftime('%Y-%m-%d')

        values = {
            'products': products_data,
            'current_date': current_date,
            'cover_image': settings.get("cover_image"),
            'enable_logo': settings.get("enable_logo"),
            'logo_position': settings.get("logo_position"),
            'logo_image': settings.get("logo_image"),
            'enable_header': settings.get("enable_header"),
            'header_text': settings.get("header_text"),
            'enable_footer': settings.get("enable_footer"),
            'footer_text': settings.get("footer_text"),
            'display_date': settings.get("display_date"),
        }

        # Render the PDF
        report_service = request.env['ir.actions.report']
        pdf_content, _ = report_service._render_qweb_pdf(
            'wbl_website_pdf_catalog.action_report_all_product_template_pdf',
            [], values)

        # Create a response to download the PDF
        response = request.make_response(pdf_content, headers=[
            ('Content-Type', 'application/pdf'),
            ('Content-Disposition', 'attachment; filename="all_products_details.pdf"'),
        ])
        return response
