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
    'name': 'Download Catalog PDF',
    'version': '18.0.1.0.0',
    'summary': 'PDF Catalog Downloadable Product Catalog Generate PDF Catalog PDF Catalog Generation Catalog App Product Catalog Customizable Catalog Templates Odoo Catalog Management View products email download product pdf Downloadable brochure PDF management',
    'description': """PDF Catalog Downloadable Product Catalog Generate PDF Catalog PDF Catalog Generation Catalog App Product Catalog Customizable Catalog Templates Odoo Catalog Management View products email download product pdf Downloadable brochure PDF management""",
    'category': 'Website',
    'author': 'Weblytic Labs',
    'company': 'Weblytic Labs',
    'website': 'https://store.weblyticlabs.com',
    'price': '',
    'currency': '',
    'depends': ['base', 'base_setup', 'website_sale', 'website', 'sale_management', 'contacts'],
    'data': [
        'views/res_config_settings_view.xml',
        'views/product_template.xml',
        'views/website_layout.xml',
        'reports/action_all_product_details_pdf.xml',
        'reports/all_product_details_pdf.xml',
        'reports/action_all_product_details_view.xml',
        'reports/all_product_details_view.xml',

    ],

    'assets': {
        'web.assets_frontend': [
            'wbl_website_pdf_catalog/static/src/js/main_button_popup.js',
        ],
    },

    'images': ['static/description/banner.gif'],
    'live_test_url': 'https://youtu.be/QmSm4Kpe554',
    'license': 'OPL-1',
    'installable': True,
    'auto_install': False,
    'application': True,
}
