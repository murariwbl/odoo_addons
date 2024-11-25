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
from odoo.addons.auth_signup.controllers.main import AuthSignupHome
from odoo import http, tools, _


class AuthSignupHomeInherit(AuthSignupHome):
    @http.route()
    def web_login(self, *args, **kw):
        # Get the email entered during login
        email = kw.get('login', '').strip()

        # Search for the partner linked to this email
        partner = request.env['res.partner'].sudo().search([('email', '=', email)], limit=1)

        # If the partner exists and is_verified is False, redirect to login with an error message
        if partner and not partner.is_verified:
            return request.render('web.login', {
                'error': 'Your account is not verified. Please verify your email before logging in.'
            })

        # Allow login if the partner is verified
        return super(AuthSignupHomeInherit, self).web_login(*args, **kw)


class AuthSignupHomeLogin(AuthSignupHome):
    @http.route('/web/signup', type='http', auth='public', website=True, sitemap=False)
    def web_auth_signup(self, *args, **kw):
        res = super(AuthSignupHomeLogin, self).web_auth_signup(*args, **kw)

        # Check if the request method is POST (account creation)
        if request.httprequest.method == 'POST':
            # Fetch the recently created user using the session UID
            if request.session.uid:
                user_id = request.env['res.users'].sudo().browse(request.session.uid)
                if user_id:
                    partner_email = user_id.partner_id.email  # Get the email of the newly created user

                    # Fetch the admin's email dynamically in sudo mode
                    admin_user = request.env.ref('base.user_admin').sudo()
                    admin_email = admin_user.partner_id.email

                    # Fetch the email template
                    template = request.env.ref('wbl_email_verification.email_user_verify')

                    # Prepare email values
                    email_values = {
                        'email_to': partner_email,  # Recipient email
                        'email_from': admin_email  # Sender email (admin email)
                    }

                    # Send the email
                    template.send_mail(user_id.partner_id.id, force_send=True, email_values=email_values)

                # Log out the session and redirect to the login page
                request.session.logout(keep_db=True)
                return request.redirect('/web/login')

        return res

