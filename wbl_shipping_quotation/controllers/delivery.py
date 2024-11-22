from odoo import http
from odoo.http import request


class DeliveryCarrierController(http.Controller):
    @http.route('/custom/get_delivery_carrier', type='json', auth='public', methods=['POST'])
    def get_delivery_carrier(self, dm_id=None):
        if not dm_id:
            return {'error': 'dm_id is required'}

        carrier = request.env['delivery.carrier'].sudo().search([('id', '=', dm_id)], limit=1)
        if not carrier:
            return {'error': 'Carrier not found'}

        # Retrieve the current sale order from the session
        sale_order = request.env['sale.order'].sudo().search([('id', '=', request.session.get('sale_order_id'))],
                                                             limit=1)
        if not sale_order:
            return {'error': 'No active sale order'}

        # Fetch the shipping price from the carrier.quotation model
        quotation = request.env['carrier.quotation'].sudo().search([('carrier_id', '=', carrier.id)], limit=1)
        shipping_price = quotation.shipping_price if quotation else 0.0
        # print("====shipping_price=====", shipping_price)

        # Include shipping price in the result
        result = {
            'enable_quotation': carrier.enable_quotation,
            'require_message_box': carrier.require_message_box,
            'message_show': carrier.message_show,
            'custom_message': carrier.custom_message,
            'button_name': carrier.button_name,
            'shipping_quotation': sale_order.shipping_quotation,
            'shipping_price': shipping_price,  # Shipping price from carrier.quotation
        }
        return result

# from odoo import http
# from odoo.http import request
#
#
# class DeliveryCarrierController(http.Controller):
#     @http.route('/custom/get_delivery_carrier', type='json', auth='public', methods=['POST'])
#     def get_delivery_carrier(self, dm_id=None):
#         if not dm_id:
#             return {'error': 'dm_id is required'}
#
#         carrier = request.env['delivery.carrier'].sudo().search([('id', '=', dm_id)], limit=1)
#         print("===carrier==", carrier,)
#         if not carrier:
#             return {'error': 'Carrier not found'}
#
#         # Retrieve the current sale order from the session
#         sale_order = request.env['sale.order'].sudo().search([('id', '=', request.session.get('sale_order_id'))],
#                                                              limit=1)
#         if not sale_order:
#             return {'error': 'No active sale order'}
#         # Check if the `shipping_quotation` field is True or False in the sale order
#         if sale_order.shipping_quotation:
#             print(sale_order.shipping_quotation)
#         else:
#             print(sale_order.shipping_quotation)
#
#
#         result = {
#             'enable_quotation': carrier.enable_quotation,
#             'require_message_box': carrier.require_message_box,
#             'message_show': carrier.message_show,
#             'custom_message': carrier.custom_message,
#             'button_name': carrier.button_name,
#             'shipping_quotation': sale_order.shipping_quotation,
#         }
#         return result

# from odoo import http
# from odoo.http import request
#
# class DeliveryCarrierController(http.Controller):
#     @http.route('/custom/get_delivery_carrier', type='json', auth='public', methods=['POST'])
#     def get_delivery_carrier(self, dm_id=None):
#         if not dm_id:
#             return {'error': 'dm_id is required'}
#
#         carrier = request.env['delivery.carrier'].sudo().search([('id', '=', dm_id)], limit=1)
#         result = {
#             'enable_quotation': carrier.enable_quotation,
#             'require_message_box': carrier.require_message_box,
#             'message_show': carrier.message_show,
#             'custom_message': carrier.custom_message,
#             'button_name': carrier.button_name,
#         }
#         return result
