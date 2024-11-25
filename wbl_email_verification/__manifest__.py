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
    'name': 'Email Verification',
    'version': '17.0.1.0.0',
    'summary': 'User account security Mandatory email confirmation email verification app User registration security user authentication guest email verify prevent fake email registration Unverified user restrictions.',
    'description': """User account security Mandatory email confirmation email verification app User registration security user authentication guest email verify prevent fake email registration Unverified user restrictions.""",
    'category': 'Website',
    'author': 'Weblytic Labs',
    'company': 'Weblytic Labs',
    'website': 'https://store.weblyticlabs.com',
    'depends': ['base','base_setup', 'contacts', 'mail', 'web', 'website', 'website_sale', 'auth_signup', 'portal'],
    'price': '25.00',
    'currency': 'USD',
    'data': [
        'security/ir.model.access.csv',
        'data/email_template.xml',
        'views/sub_menu.xml',
        'views/res_config_settings.xml',
    ],
    'images': ['static/description/banner.gif'],
    'live_test_url': 'https://youtu.be/-f2dsGdjk2I',
    'license': 'OPL-1',
    'installable': True,
    'auto_install': False,
    'application': True,
}
