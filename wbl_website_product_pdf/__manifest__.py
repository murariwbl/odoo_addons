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
    'name': 'Website Product Pdf',
    'version': '17.0.1.0.0',
    'summary': '',
    'sequence': 1,
    'description': """""",
    'category': '',
    'author': 'Weblytic Labs',
    'company': 'Weblytic Labs',
    'website': 'https://store.weblyticlabs.com',
    'price': '',
    'currency': '',
    'depends': ['base', 'web', 'base_setup', 'sale_management', 'purchase', 'stock', 'mrp', 'website_sale',
                'website', 'portal', 'product'],
    'data': [
        'views/product_template.xml',
        'views/product_details_view.xml',
        'views/product_details_action.xml',
        'reports/product_details_pdf.xml',
        'reports/action_report.xml',

    ],
    'assets': {
        'web.assets_frontend': [
            'wbl_website_product_pdf/static/src/js/product_form.js',
        ],
    },
    'license': 'OPL-1',
    'installable': True,
    'auto_install': False,
    'application': True,
}
