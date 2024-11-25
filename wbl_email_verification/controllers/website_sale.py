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
from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.addons.web.controllers.home import Home
from odoo.addons.website.controllers.main import Website
from odoo.http import content_disposition, Controller, request, route
from odoo.http import request
from odoo import http, tools, _


class WebsiteSaleInherit(WebsiteSale):

    @http.route(['/shop', '/shop/page/<int:page>', '/shop/category/<model("product.public.category"):category>',
                 '/shop/category/<model("product.public.category"):category>/page/<int:page>'], type='http',
                auth="public", website=True, sitemap=False)
    def shop(self, page=0, category=None, search='', min_price=0.0, max_price=0.0, ppg=False, **post):
        response = super(WebsiteSaleInherit, self).shop(page, category, search, min_price, max_price, ppg, **post)
        settings = request.env['res.config.settings'].sudo().get_values()
        is_marque = settings.get("marque_notice")
        user_id = request.env['res.users'].sudo().browse(request.session.uid)
        verify_user = user_id.partner_id.is_verified
        values = {
            'marquee_text': settings.get("marque_text"),
            'marquee_bg_color': settings.get("bar_color"),
            'marquee_text_color': settings.get("text_color"),
            'hide_price': settings.get("hide_price"),
        }
        if is_marque:
            if not verify_user:
                response.qcontext.update(values)
        return response

    @http.route(['/shop/cart'], type='http', auth="public", website=True, sitemap=False)
    def cart(self, access_token=None, revive='', **post):
        response = super(WebsiteSaleInherit, self).cart(access_token, revive, **post)
        settings = request.env['res.config.settings'].sudo().get_values()
        is_marque = settings.get("marque_notice")
        user_id = request.env['res.users'].sudo().browse(request.session.uid)
        verify_user = user_id.partner_id.is_verified
        values = {
            'marquee_text': settings.get("marque_text"),
            'marquee_bg_color': settings.get("bar_color"),
            'marquee_text_color': settings.get("text_color"),
            'hide_price': settings.get("hide_price"),
        }
        if is_marque:
            if not verify_user:
                response.qcontext.update(values)
        return response

    def _prepare_product_values(self, product, category, search, **kwargs):
        response = super(WebsiteSaleInherit, self)._prepare_product_values(product, category, search, **kwargs)
        settings = request.env['res.config.settings'].sudo().get_values()
        user_id = request.env['res.users'].sudo().browse(request.session.uid)
        verify_user = user_id.partner_id.is_verified
        response['hide_add_to_cart'] = True if not verify_user and settings.get("hide_cart") else False
        response['hide_price'] = True if not verify_user and settings.get("hide_price") else False
        return response

    @http.route(['/shop/<model("product.template"):product>'], type='http', auth="public", website=True, sitemap=True)
    def product(self, product, category='', search='', **kwargs):
        response = super(WebsiteSaleInherit, self).product(product, category, search, **kwargs)
        settings = request.env['res.config.settings'].sudo().get_values()
        is_marque = settings.get("marque_notice")
        user_id = request.env['res.users'].sudo().browse(request.session.uid)
        verify_user = user_id.partner_id.is_verified
        values = {
            'marquee_text': settings.get("marque_text"),
            'marquee_bg_color': settings.get("bar_color"),
            'marquee_text_color': settings.get("text_color"),
            'hide_price': settings.get("hide_price"),
        }
        if is_marque:
            if not verify_user:
                response.qcontext.update(values)
        return response

    @http.route('/shop/payment', type='http', auth='public', website=True, sitemap=False)
    def shop_payment(self, **post):
        response = super(WebsiteSaleInherit, self).shop_payment(**post)
        settings = request.env['res.config.settings'].sudo().get_values()
        is_marque = settings.get("marque_notice")
        user_id = request.env['res.users'].sudo().browse(request.session.uid)
        verify_user = user_id.partner_id.is_verified
        values = {
            'marquee_text': settings.get("marque_text"),
            'marquee_bg_color': settings.get("bar_color"),
            'marquee_text_color': settings.get("text_color"),
            'hide_price': settings.get("hide_price"),
        }
        if is_marque:
            if not verify_user:
                response.qcontext.update(values)
        return response


class CustomWebsite(Website):

    @http.route('/', type='http', auth='public', website=True)
    def index(self, **kwargs):
        response = super(CustomWebsite, self).index(**kwargs)
        settings = request.env['res.config.settings'].sudo().get_values()
        is_marque = settings.get("marque_notice")
        user_id = request.env['res.users'].sudo().browse(request.session.uid)
        verify_user = user_id.partner_id.is_verified
        values = {
            'marquee_text': settings.get("marque_text"),
            'marquee_bg_color': settings.get("bar_color"),
            'marquee_text_color': settings.get("text_color"),
            'hide_price': settings.get("hide_price"),
        }
        if is_marque:
            if not verify_user:
                response.qcontext.update(values)
        return response


class CustomerPortalInherit(CustomerPortal):

    @route(['/my', '/my/home'], type='http', auth="user", website=True)
    def home(self, **kw):
        response = super(CustomerPortalInherit, self).home(**kw)
        settings = request.env['res.config.settings'].sudo().get_values()
        is_marque = settings.get("marque_notice")
        user_id = request.env['res.users'].sudo().browse(request.session.uid)
        verify_user = user_id.partner_id.is_verified
        values = {
            'marquee_text': settings.get("marque_text"),
            'marquee_bg_color': settings.get("bar_color"),
            'marquee_text_color': settings.get("text_color"),
            'hide_price': settings.get("hide_price"),
        }
        if is_marque:
            if not verify_user:
                response.qcontext.update(values)
        return response


class HomeInherit(Home):
    @http.route('/web/login', type='http', auth="public", website=True)
    def web_login(self, redirect=None, **kw):
        response = super(HomeInherit, self).web_login(redirect, **kw)
        settings = request.env['res.config.settings'].sudo().get_values()
        is_marque = settings.get("marque_notice")
        user_id = request.env['res.users'].sudo().browse(request.session.uid)
        verify_user = user_id.partner_id.is_verified
        values = {
            'marquee_text': settings.get("marque_text"),
            'marquee_bg_color': settings.get("bar_color"),
            'marquee_text_color': settings.get("text_color"),
            'hide_price': settings.get("hide_price"),
        }
        if is_marque:
            if not verify_user:
                response.qcontext.update(values)
        return response
