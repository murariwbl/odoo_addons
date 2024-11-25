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


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    marque_notice = fields.Boolean("Enable Marque")
    marque_text = fields.Text("Marque Text")
    text_color = fields.Text("Marque Text Color")
    bar_color = fields.Text("Marque Bar Color")
    hide_price = fields.Boolean("Hide Price For Unverified User")
    hide_cart = fields.Boolean("Hide Cart For Unverified User")

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        IrConfigParam = self.env['ir.config_parameter'].sudo()

        res.update(
            marque_notice=IrConfigParam.get_param('res.config.settings.marque_notice', default=False),
            marque_text=IrConfigParam.get_param('res.config.settings.marque_text', default=False),
            text_color=IrConfigParam.get_param('res.config.settings.text_color', default=False),
            bar_color=IrConfigParam.get_param('res.config.settings.bar_color', default=False),
            hide_price=IrConfigParam.get_param('res.config.settings.hide_price', default=False),
            hide_cart=IrConfigParam.get_param('res.config.settings.hide_cart', default=False),
        )
        return res

    @api.model
    def set_values(self):
        super(ResConfigSettings, self).set_values()
        IrConfigParam = self.env['ir.config_parameter'].sudo()

        IrConfigParam.set_param('res.config.settings.marque_notice', self.marque_notice)
        IrConfigParam.set_param('res.config.settings.marque_text', self.marque_text)
        IrConfigParam.set_param('res.config.settings.text_color', self.text_color)
        IrConfigParam.set_param('res.config.settings.bar_color', self.bar_color)
        IrConfigParam.set_param('res.config.settings.hide_price', self.hide_price)
        IrConfigParam.set_param('res.config.settings.hide_cart', self.hide_cart)
