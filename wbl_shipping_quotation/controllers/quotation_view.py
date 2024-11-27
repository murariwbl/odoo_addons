from odoo import http
from odoo.http import request
from datetime import datetime


# THIS CONTROLLER IS USED TO SHOW THE DATA INSIDE THE MY ACCOUNT MANAGER INSIDE SHIPPING QUOTATION
class MyPortalRmaController(http.Controller):

    @http.route('/my/shipping/quotation', website=True, auth='user')
    def portal_rma(self, **kw):
        # Get the current user
        partner = request.env.user.partner_id

        # Fetch the carrier quotations for the current user (partner)
        quotations = request.env['carrier.quotation'].sudo().search([('customer_email', '=', partner.email)])

        today_date = datetime.today().strftime('%Y-%m-%d')

        # Prepare the data to pass to the template
        quotation_data = []
        for quotation in quotations:
            # Check if expired_date is a string or date and handle accordingly
            expired_date = quotation.expired_date
            if isinstance(expired_date, str):
                formatted_expired_date = expired_date
            elif isinstance(expired_date, datetime):
                formatted_expired_date = expired_date.strftime('%Y-%m-%d')
            else:
                formatted_expired_date = None

            # print(f"Expired Date: {formatted_expired_date}, Today's Date: {today_date}")
            # print("dfdfdfdfd========",quotation.currency_id.symbol)

            data = {
                'name': quotation.name,
                'product_count': len(quotation.product_ids),  # Count of products
                'cart_id': quotation.cart_id,
                'customer_name': quotation.customer_name,
                'customer_email': quotation.customer_email,
                'total': quotation.total,
                'carrier': quotation.carrier,
                'status': quotation.status,
                'shipping_price': quotation.shipping_price,
                'Received_date': quotation.Received_date,
                'expired_date': quotation.expired_date,
                'today_date': today_date,
                'currency_symbol': quotation.currency_id.symbol if quotation.currency_id else '',
            }
            quotation_data.append(data)

        # Values to be passed to the template
        values = {
            'quotation_details': quotation_data,
        }

        return request.render('wbl_shipping_quotation.wbl_my_portal_quotation_view', values)

    # @http.route('/my/shipping/quotation', website=True, auth='user')
    # def portal_rma(self, **kw):
    #     print("=======button trigger")
    #     # Get the current user
    #     partner = request.env.user.partner_id
    #
    #     # Fetch the carrier quotations for the current user (partner)
    #     quotations = request.env['carrier.quotation'].sudo().search([('customer_email', '=', partner.email)])
    #
    #     today_date = datetime.today().strftime('%Y-%m-%d')
    #
    #     # Prepare the data to pass to the template
    #     quotation_data = []
    #     for quotation in quotations:
    #         data = {
    #             'name': quotation.name,
    #             'product_count': len(quotation.product_ids),  # Count of products
    #             'cart_id': quotation.cart_id,
    #             'customer_name': quotation.customer_name,
    #             'customer_email': quotation.customer_email,
    #             'total': quotation.total,
    #             'carrier': quotation.carrier,
    #             'status': quotation.status,
    #             'shipping_price': quotation.shipping_price,
    #             'Received_date': quotation.Received_date,
    #             'expired_date': quotation.expired_date.strftime('%Y-%m-%d') if quotation.expired_date else None,  # Ensure proper formatting
    #             'today_date': today_date,
    #
    #         }
    #         quotation_data.append(data)
    #
    #     # Values to be passed to the template
    #     values = {
    #         'quotation_details': quotation_data,
    #     }
    #
    #     return request.render('wbl_shipping_quotation.wbl_my_portal_quotation_view', values)
