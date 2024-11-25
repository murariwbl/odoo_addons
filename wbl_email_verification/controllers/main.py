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

from odoo import http
from odoo.http import request
from odoo import http, tools, _


class AccountVerifications(http.Controller):

    @http.route('/email/verification/<int:partner_id>', type='http', auth='user', methods=['GET'])
    def verify_account(self, partner_id):
        if partner_id:
            res_partner = request.env['res.partner'].browse(partner_id)
            res_partner.is_verified = True
        return request.redirect('/')
