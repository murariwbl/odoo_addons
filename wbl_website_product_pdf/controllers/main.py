from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal


##############   THIS CONTROLLER IS USED TO PRINT THE PRODUCT PDF ON PRINT BUTTON CLICK ############
class PortalMyProductDetailsPdf(http.Controller):
    @http.route(['/product/details/pdf'], methods=["GET"], auth='public', website=True)
    def portal_my_product_details_pdf(self, product_id, **kw):
        # Fetch the product record using the product_id
        product = request.env['product.template'].sudo().browse(int(product_id))

        # Collect attributes and values
        attributes = []
        for attribute_line in product.attribute_line_ids:
            attribute = attribute_line.attribute_id
            print("Attribute Fetched:", attribute.name)  # Check if attributes are fetched

            for value in attribute_line.value_ids:
                print(" - Value Fetched:", value.name)  # Check if values are fetched
                attributes.append({
                    'attribute': attribute.name,
                    'value': value.name
                })

        currency_symbol = product.currency_id.symbol or ''  # Fetch product currency symbol
        formatted_price = f"{product.list_price:.2f}"  # Format the price to two decimal places

        values = {
            'product': product,
            'name': product.name,
            'list_price': formatted_price,
            'currency_symbol': currency_symbol,
            'image': product.image_1920,
            'description': product.description_sale or '',
            'attributes': attributes,
        }
        # Generate the PDF using the 'ir.actions.report' service with the correct report action ID
        report_service = request.env['ir.actions.report']
        pdf_content, _ = report_service._render_qweb_pdf('wbl_website_product_pdf.action_report_product_template',
                                                         [product.id], values)

        # Create a response that triggers the file download
        response = request.make_response(pdf_content, headers=[
            ('Content-Type', 'application/pdf'),
            ('Content-Disposition', f'attachment; filename="{product.name}_details.pdf"'),
        ])

        return response


##############   THIS CONTROLLER IS USED TO VIEW THE PRODUCT DETAILS ON VIEW BUTTON CLICK ############
class PortalMyProductDetails(CustomerPortal):

    @http.route(['/product/details'], methods=["GET"], type='http', auth='public', website=True)
    def portal_my_product_details(self, product_id, **kw):
        print("============ Route Triggered ============")  # Check if this prints
        if product_id:
            product = request.env['product.template'].sudo().browse(int(product_id))
            print("Product Fetched:", product)  # Check if the product is fetched

            # Collect attributes and values
            attributes = []
            for attribute_line in product.attribute_line_ids:
                attribute = attribute_line.attribute_id
                print("Attribute Fetched:", attribute.name)  # Check if attributes are fetched

                for value in attribute_line.value_ids:
                    print(" - Value Fetched:", value.name)  # Check if values are fetched
                    attributes.append({
                        'attribute': attribute.name,
                        'value': value.name
                    })

            # Get other product details
            currency_symbol = product.currency_id.symbol or ''
            formatted_price = f"{product.list_price:.2f}"

            # Pass all values to the template
            values = {
                'product': product,
                'name': product.name,
                'list_price': formatted_price,
                'currency_symbol': currency_symbol,
                'image': product.image_1920,
                'description': product.description_sale or '',
                'attributes': attributes,
            }
            print("Values to Render:", values)  # Print values before rendering

            # Generate PDF using QWeb template
            pdf_content, _ = request.env['ir.actions.report']._render_qweb_pdf(
                'wbl_website_product_pdf.template_products_details_action', [product.id], values)

            # Create PDF response
            response = request.make_response(pdf_content, headers=[
                ('Content-Type', 'application/pdf'),
            ])

            return response
        return request.not_found()
