from odoo import http
from odoo.http import request
import re



# THIS CONTROLLER IS USED FOR WHEN WE CLICK THE VIEW LOGO INSIDE THE ACCOUNT MANAGER OF SHIPPING COST
class PortalMyProductDetailsPdf(http.Controller):

    @http.route(['/shipping/quotation/view'], type='http', auth='public', website=True)
    def portal_my_product_details_pdf(self, **kw):
        # Get the quotation_id from the URL parameters
        order = request.website.sale_get_order()
        print(order.order_line)
        quotation_id = kw.get('quotation_id')
        print("=======View button clicked")
        print("=======Quotation ID:", quotation_id)

        # Fetch the quotation record from the database using the quotation ID
        quotation = request.env['carrier.quotation'].sudo().search([('name', '=', quotation_id)], limit=1)
        current_partner_id = request.env.user.partner_id.name
        print("==current_partner_id====", current_partner_id)

        # Check if a sale order exists with this quotation_id
        sale_order = request.env['sale.order'].sudo().search([('quotation_id', '=', quotation.id)], limit=1)
        sale_order_exists = bool(sale_order)

        # Check if order and currency_id exist
        currency_symbol = quotation.currency_id.symbol
        # Debugging the currency symbol
        if not currency_symbol:
            print("Currency symbol could not be determined from the order.")
        else:
            print(f"Currency symbol: {currency_symbol}")

        # Prepare product details
        product_lines = []
        # currency_symbol = str(order.currency_id.symbol) if isinstance(order.currency_id.symbol, str) else ''

        for product_line in quotation.product_ids:
            # Ensure Total is a string
            line_total = str(product_line.Total or '0')

            # Clean line_total using regex to remove currency symbols and commas
            try:
                # Remove known currency symbol
                if currency_symbol:
                    line_total = line_total.replace(currency_symbol, '')

                # Use regex to keep only numbers and the decimal point
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
            print("====product_image====", product_image)

            # Append cleaned data to product lines
            product_lines.append({
                'product_id': product_line.product_id.id,
                'product_name': product_line.product_id.name,
                'unit_price': product_line.unit_price,
                'product_quantity': product_line.product_quantity,
                'total': line_total,
                'image_128': product_image,
            })

            # Debugging
            print("Product:", product_line.product_id.name)
            print("Total (as float):", line_total)
            print("--------------------")

        # Access partner details
        partner_name = request.env.user.partner_id.name
        partner_address = request.env.user.partner_id.contact_address  # Assuming 'contact_address' is a field
        partner_phone = request.env.user.partner_id.phone
        partner_email = request.env.user.partner_id.email

        # Calculate subtotal
        total_products_amount = sum(float(line['total']) for line in product_lines)
        shipping_price = float(quotation.shipping_price or 0.0)
        subtotal = total_products_amount + shipping_price
        print("====subtotal", subtotal)

        print("Product Lines:", product_lines)
        print("Quotation Status:", quotation.status)
        print("Quotation ID:", quotation.id)

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
            # 'quotation_id': quotation.id,
        }

        # Clear the cart after rendering the quotation details
        if order:
            order._clear_cart()
            print("Cart cleared successfully.")

        return request.render('wbl_shipping_quotation.template_quotation_details', values)

# class PortalMyProductDetailsPdf(http.Controller):
#
#     @http.route(['/shipping/quotation/view'], type='http', auth='public', website=True)
#     def portal_my_product_details_pdf(self, **kw):
#         # Get the quotation_id from the URL parameters
#         order = request.website.sale_get_order()
#         print(order.order_line)
#         quotation_id = kw.get('quotation_id')
#         print("=======View button clicked")
#         print("=======Quotation ID:", quotation_id)
#
#         # Fetch the quotation record from the database using the quotation ID
#         quotation = request.env['carrier.quotation'].sudo().search([('name', '=', quotation_id)], limit=1)
#         current_partner_id = request.env.user.partner_id.name
#         print("==current_partner_id====", current_partner_id)
#
#         # Prepare product details
#         product_lines = []
#         for product_line in quotation.product_ids:
#             line_total = float(product_line.Total or 0.0)
#
#             product_lines.append({
#                 'product_id': product_line.product_id.id,
#                 'product_name': product_line.product_id.name,
#                 'unit_price': product_line.unit_price,
#                 'product_quantity': product_line.product_quantity,
#                 'total': line_total,
#             })
#             # Debugging log
#             print("== Product Line ==")
#             print("Product ID:", product_line.product_id.id)
#             print("Product Name:", product_line.product_id)
#             print("Unit Price:", product_line.unit_price)
#             print("Product Quantity:", product_line.product_quantity)
#             print("Total:", product_line.Total)
#             print("Total:", line_total)
#
#             print("--------------------")
#
#         # Access partner details
#         partner_name = request.env.user.partner_id.name
#         partner_address = request.env.user.partner_id.contact_address  # Assuming 'contact_address' is a field
#         partner_phone = request.env.user.partner_id.phone
#         partner_email = request.env.user.partner_id.email
#
#         # Calculate subtotal
#         # Calculate subtotal
#         total_products_amount = sum(float(line['total']) for line in product_lines)
#         shipping_price = float(quotation.shipping_price or 0.0)
#         subtotal = total_products_amount + shipping_price
#         print("====subtotal", subtotal)
#
#         print("Product Lines:", product_lines)
#         print("Quotation Status:", quotation.status)
#         print("Quotation ID:", quotation.id)
#
#         # sale_order = request.website.sale_get_order(force_create=True)
#         # shipping_quotation = sale_order.shipping_quotation = True
#
#         values = {
#             'quotation': quotation,
#             'customer_name': quotation.customer_name,
#             'customer_email': quotation.customer_email,
#             'carrier': quotation.carrier,
#             'Received_date': quotation.Received_date,
#             'expired_date': quotation.expired_date,
#             'message': quotation.message,
#             'status': quotation.status,
#             'partner_name': partner_name,
#             'partner_address': partner_address,
#             'partner_phone': partner_phone,
#             'partner_email': partner_email,
#             'total': quotation.total,
#             'shipping_price': quotation.shipping_price,
#             'product_lines': product_lines,  # Add product lines to the context
#             'subtotal' : subtotal,
#             'total_products_amount' : total_products_amount,
#         }
#
#         # Clear the cart after rendering the quotation details
#         if order:
#             order._clear_cart()
#             print("Cart cleared successfully.")
#
#         return request.render('wbl_shipping_quotation.template_quotation_details', values)
