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


from odoo import api, fields, models


class RmaReason(models.Model):
    _name = "rma.reason"

    name = fields.Char(string="Name", required=True)
    request_type = fields.Char(string="Request Type", required=True)
    is_published = fields.Boolean(string='Is Published', default=True)

    def published_button(self):
        self.is_published = not self.is_published
