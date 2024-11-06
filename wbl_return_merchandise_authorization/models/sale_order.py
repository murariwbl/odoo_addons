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


from odoo import api, fields, models, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_open_create_rma_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('CREATE RMA'),
            'res_model': 'rma.order.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_user_id': self.partner_id.id},
        }
