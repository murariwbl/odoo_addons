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

{
    'name': 'Return Merchandise Authorization',
    'version': '17.0.1.0.0',
    'summary': """Manager referral codes Manager assignment Customer support Customer-manager linking Account manager Customer relation manager support ticket helpdesk after sale support customer satisfaction Customer issue resolution Support team Customer loyalty Customer manager Assign manager to customer """,
    'sequence': 1,
    'description': """RMA system return management Product returns Return authorization Exchange Order Refund order Order Return Policy RMA Return Order management Return merchandise management Return tracking Return Order Rejection Order replacement Return period Order return by customer Exchange request by customer""",
    'category': 'Warehouse',
    'author': 'Weblytic Labs',
    'company': 'Weblytic Labs',
    'website': 'https://store.weblyticlabs.com',
    'price': '',
    'currency': '',
    'depends': ['base', 'web', 'base_setup', 'sale_management', 'purchase', 'stock', 'mrp', 'website_sale',
                'website', 'mail', 'portal', 'product'],
    'data': [
        'security/ir.model.access.csv',
        'data/rma_sequence.xml',
        'data/order_confirm_email_template.xml',
        'data/order_email_template.xml',
        'views/rma_order_view.xml',
        'views/rma_reason_view.xml',
        'views/rma_stages_view.xml',
        'views/rma_menus.xml',
        'views/sale_order_view.xml',
        'views/sale_portal_template.xml',
        'views/sale_portal_template_view.xml',
        'views/my_account_rma_view.xml',
        'views/my_portal_rma_orders_view.xml',
        'views/my_rma_details_view.xml',
        'wizard/rma_order_wizard_view.xml',

    ],
    'assets': {
        'web.assets_frontend': [
            'wbl_return_merchandise_authorization/static/src/js/rma_form.js',
            'wbl_return_merchandise_authorization/static/src/css/style.css',
        ],
    },
    'license': 'OPL-1',
    'installable': True,
    'auto_install': False,
    'application': True,
}
