from odoo import http
from odoo.http import request


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

        # Prepare product details
        product_lines = []
        for product_line in quotation.product_ids:
            # Remove currency symbol and convert to float
            line_total = product_line.Total
            if isinstance(line_total, str):  # Check if Total is a string
                line_total = line_total.replace(order.currency_id.symbol, '').replace(',',
                                                                                      '').strip()  # Remove currency symbol and commas
            line_total = float(line_total or 0.0)

            product_lines.append({
                'product_id': product_line.product_id.id,
                'product_name': product_line.product_id.name,
                'unit_price': product_line.unit_price,
                'product_quantity': product_line.product_quantity,
                'total': line_total,
            })
            # Debugging log
            print("== Product Line ==")
            print("Product ID:", product_line.product_id.id)
            print("Product Name:", product_line.product_id)
            print("Unit Price:", product_line.unit_price)
            print("Product Quantity:", product_line.product_quantity)
            print("Total:", product_line.Total)
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
            'currency_symbol': order.currency_id.symbol,
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
