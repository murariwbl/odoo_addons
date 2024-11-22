from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


############## THIS CONTROLLER WORK WHEN CLICK ON ADD TO CART BUTTON ################3
class CustomWebsiteSale(WebsiteSale):
    @http.route(['/shop/cart/update'], type='http', auth="public", website=True)
    def cart_update(self, product_ids=None, quantities=None, **kwargs):
        """Handle adding multiple products to the cart."""
        order = request.website.sale_get_order(force_create=True)
        if not order:
            return request.redirect('/shop')

        # Ensure product_ids and quantities are lists
        product_ids = request.httprequest.form.getlist('product_ids[]')
        quantities = request.httprequest.form.getlist('quantities[]')
        quotation_id_list = request.httprequest.form.getlist('quotation_id')

        # Convert to appropriate types
        product_ids = list(map(int, product_ids))
        quantities = list(map(float, quantities))

        # Add each product to the cart
        for product_id, quantity in zip(product_ids, quantities):
            order._cart_update(product_id=product_id, add_qty=quantity)

        # Update the sale order with quotation details if available
        if quotation_id_list:
            quotation_id = int(quotation_id_list[0])  # Retrieve the first value
            quotation = request.env['carrier.quotation'].sudo().browse(quotation_id)
            order.write({
                'quotation_id': quotation.id,
            })

        order.shipping_quotation = True

        return request.redirect('/shop/cart')


############ THE CONTROLLER UPDATE THE SHIPPING PRICE INSIDE THE SHIPPING METHOD #####################
class CustomWebsiteSaleCheckout(WebsiteSale):
    @http.route('/shop/checkout', type='http', methods=['GET'], auth='public', website=True, sitemap=False)
    def shop_checkout(self, **query_params):
        print("=====shop_checkout function triggered=====")

        # Fetch the current sale order (reload from database to ensure we have the latest data)
        sale_order = request.website.sale_get_order()
        if sale_order:
            # Reload the sale order to ensure its data is fresh, including the order lines
            sale_order = request.env['sale.order'].browse(sale_order.id)
            print("=====sale_order=====", sale_order)

            # Ensure that the order lines are loaded and the 'is_delivery' field is set
            sale_order = sale_order.sudo()  # Use sudo if necessary to bypass access rights

            # Find the delivery product line (where is_delivery is True)
            delivery_line = sale_order.order_line.filtered(lambda line: line.is_delivery)
            print("=========delivery_line=", delivery_line)

            if delivery_line:
                print("=======Delivery Lines=======")
                for line in delivery_line:
                    print(
                        f"Delivery Product: {line.product_id.name}, Line ID: {line.id}, is_delivery: {line.is_delivery}")

                # Check if the sale order has a valid quotation_id
                if sale_order.quotation_id:
                    # Get the related carrier.quotation record
                    carrier_quotation = sale_order.quotation_id
                    print("====carrier_quotation===", carrier_quotation)
                    print("====sale_order.quotation_id.id===", sale_order.quotation_id.id)

                    # Ensure the ID of quotation_id matches the one in the carrier.quotation model
                    if carrier_quotation.id == sale_order.quotation_id.id:
                        # If there's a shipping_price, update the price_unit of the delivery line
                        if carrier_quotation.shipping_price:
                            print(f"Updating price_unit with shipping price: {carrier_quotation.shipping_price}")
                            for line in delivery_line:
                                line.write({
                                    'price_unit': carrier_quotation.shipping_price
                                })
            else:
                print("No delivery line found in the sale order")
        else:
            print("No active sale order found")

        # Continue with the original checkout process
        return super(CustomWebsiteSaleCheckout, self).shop_checkout(**query_params)

# class CustomWebsiteSaleCheckout(WebsiteSale):
#     @http.route('/shop/checkout', type='http', methods=['GET'], auth='public', website=True, sitemap=False)
#     def shop_checkout(self, **query_params):
#         print("=====shop_checkout function trigger=====")
#         # Fetch the current sale order
#         sale_order = request.website.sale_get_order()
#         print("=====sale_order=====", sale_order)
#
#         if sale_order:
#             # Find the delivery product line (where is_delivery is True)
#             delivery_line = sale_order.order_line.filtered(lambda line: line.is_delivery)
#             print("=========delivery_line=", delivery_line)
#
#             if delivery_line:
#                 print("=======Delivery Lines=======")
#                 for line in delivery_line:
#                     print(
#                         f"Delivery Product: {line.product_id.name}, Line ID: {line.id}, is_delivery: {line.is_delivery}")
#
#                 # Check if the sale order has a valid quotation_id
#                 if sale_order.quotation_id:
#                     # Get the related carrier.quotation record
#                     carrier_quotation = sale_order.quotation_id
#                     print("====carrier_quotation===", carrier_quotation)
#                     print("====sale_order.quotation_id.id===", sale_order.quotation_id.id)
#
#                     # Ensure the ID of quotation_id matches the one in the carrier.quotation model
#                     if carrier_quotation.id == sale_order.quotation_id.id:
#                         # If there's a shipping_price, update the price_unit of the delivery line
#                         if carrier_quotation.shipping_price:
#                             print(f"Updating price_unit with shipping price: {carrier_quotation.shipping_price}")
#                             for line in delivery_line:
#                                 line.write({
#                                     'price_unit': carrier_quotation.shipping_price
#                                 })
#             else:
#                 print("No delivery line found in the sale order")
#         else:
#             print("No active sale order found")
#
#         # Continue with the original checkout process
#         return super(CustomWebsiteSaleCheckout, self).shop_checkout(**query_params)
