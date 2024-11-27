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

    enable_pdf = fields.Boolean("Enable PDF Catalog")
    enable_pdf_product = fields.Boolean("Enable PDF Product Page")
    # button_name = fields.Text("Button Name")
    cover_image = fields.Binary("Cover Image")
    enable_logo = fields.Boolean("Enable Shop Logo")
    logo_position = fields.Selection([
        ("left", "Left"),
        ("center", "Center"),
        ("right", "Right")], string="Logo Position in header")
    logo_image = fields.Binary("Logo Image")
    enable_header = fields.Boolean("Enable Header")
    header_text = fields.Text(string="Header Text")
    enable_footer = fields.Boolean("Enable footer")
    footer_text = fields.Text(string="Footer Text")
    display_date = fields.Boolean("Display Date In Header")
    # enable_pdf_product = fields.Boolean("Enable Pdf On Product Page")
    # enable_pdf_category = fields.Boolean("Enable Pdf On Category Page")

    # customer_ids = fields.Many2many('res.partner', string='Allowed Customers')
    category_ids = fields.Many2many('product.category', string="Categories")

    # product_ids = fields.Many2many('product.template', string="Products")

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        IrConfigParam = self.env['ir.config_parameter'].sudo()

        # Fetch the stored customer, category, and product IDs
        customer_ids_str = IrConfigParam.get_param('res.config.settings.customer_ids', default=False)
        category_ids_str = IrConfigParam.get_param('res.config.settings.category_ids', default=False)
        product_ids_str = IrConfigParam.get_param('res.config.settings.product_ids', default=False)

        # customer_ids = customer_ids_str and [int(cid) for cid in customer_ids_str.split(',')] or []
        category_ids = category_ids_str and [int(cid) for cid in category_ids_str.split(',')] or []
        # product_ids = product_ids_str and [int(pid) for pid in product_ids_str.split(',')] or []

        res.update(
            enable_pdf=IrConfigParam.get_param('res.config.settings.enable_pdf', default=False),
            enable_pdf_product=IrConfigParam.get_param('res.config.settings.enable_pdf_product', default=False),
            cover_image=IrConfigParam.get_param('res.config.settings.cover_image', default=False),
            enable_logo=IrConfigParam.get_param('res.config.settings.enable_logo', default=False),
            logo_position=IrConfigParam.get_param('res.config.settings.logo_position', default=False),
            logo_image=IrConfigParam.get_param('res.config.settings.logo_image', default=False),
            header_text=IrConfigParam.get_param('res.config.settings.header_text', default=False),
            enable_header=IrConfigParam.get_param('res.config.settings.enable_header', default=False),
            footer_text=IrConfigParam.get_param('res.config.settings.footer_text', default=False),
            enable_footer=IrConfigParam.get_param('res.config.settings.enable_footer', default=False),
            display_date=IrConfigParam.get_param('res.config.settings.display_date', default=False),
            # enable_pdf_product=IrConfigParam.get_param('res.config.settings.enable_pdf_product', default=False),
            # enable_pdf_category=IrConfigParam.get_param('res.config.settings.enable_pdf_category', default=False),

            # Set Many2many fields with the IDs
            # customer_ids=[(6, 0, customer_ids)],
            category_ids=[(6, 0, category_ids)],
            # product_ids=[(6, 0, product_ids)],
        )
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        IrConfigParam = self.env['ir.config_parameter'].sudo()

        IrConfigParam.set_param('res.config.settings.enable_pdf', self.enable_pdf)
        IrConfigParam.set_param('res.config.settings.enable_pdf_product', self.enable_pdf_product)
        IrConfigParam.set_param('res.config.settings.cover_image', self.cover_image)
        IrConfigParam.set_param('res.config.settings.enable_logo', self.enable_logo)
        IrConfigParam.set_param('res.config.settings.logo_position', self.logo_position)
        IrConfigParam.set_param('res.config.settings.logo_image', self.logo_image)
        IrConfigParam.set_param('res.config.settings.enable_header', self.enable_header)
        IrConfigParam.set_param('res.config.settings.header_text', self.header_text)
        IrConfigParam.set_param('res.config.settings.enable_footer', self.enable_footer)
        IrConfigParam.set_param('res.config.settings.footer_text', self.footer_text)
        IrConfigParam.set_param('res.config.settings.display_date', self.display_date)
        # IrConfigParam.set_param('res.config.settings.enable_pdf_product', self.enable_pdf_product)
        # IrConfigParam.set_param('res.config.settings.enable_pdf_category', self.enable_pdf_category)

        # Store customer, category, and product IDs as comma-separated strings
        # customer_ids_str = ','.join(map(str, self.customer_ids.ids))
        category_ids_str = ','.join(map(str, self.category_ids.ids))
        # product_ids_str = ','.join(map(str, self.product_ids.ids))

        # IrConfigParam.set_param('res.config.settings.customer_ids', customer_ids_str)
        IrConfigParam.set_param('res.config.settings.category_ids', category_ids_str)
        # IrConfigParam.set_param('res.config.settings.product_ids', product_ids_str)
