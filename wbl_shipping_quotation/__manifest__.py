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
    'name': 'Shipping Quotation',
    'version': '18.0.1.0.0',
    'summary': "",
    'sequence': 1,
    'description': """""",
    'category': '',
    'author': 'Weblytic Labs',
    'company': 'Weblytic Labs',
    'website': 'https://store.weblyticlabs.com',
    'price': '',
    'currency': '',
    'depends': ['base', 'base_setup', 'sale_management', 'delivery', 'website', 'website_sale'],

    'data': [
        'security/ir.model.access.csv',
        'views/delivery_carier_view.xml',
        'views/delivery_form_template.xml',
        'views/carrier_quotation_view.xml',
        'views/my_account_carrier_quotation_view.xml',
        'views/my_quotation_view.xml',
        'views/menus_view.xml',
        'views/ir_cron_action.xml',
        'reports/shipping_quotation_report.xml',
        'reports/action_shipping_quotation_report_don.xml',
        'reports/shipping_quotation_report_donload.xml',
    ],

    'assets': {
        'web.assets_frontend': [
            'wbl_shipping_quotation/static/src/js/shipping_form.js',
            'wbl_shipping_quotation/static/src/js/shipping_quotation.js',
        ],
    },

    'images': ['static/description/banner.gif'],
    'license': 'OPL-1',
    'installable': True,
    'auto_install': False,
    'application': True,
}
