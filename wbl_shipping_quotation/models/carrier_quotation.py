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
from datetime import date, datetime, time
import logging

_logger = logging.getLogger(__name__)


class CarrierQuotation(models.Model):
    _name = "carrier.quotation"

    name = fields.Char(string="Reference")
    cart_id = fields.Char(string="Cart Id")
    status = fields.Selection(
        [('open', 'Open'), ('sent', 'Sent')], default='open', string="status")
    customer_name = fields.Char(string="Customer Name")
    customer_email = fields.Char(string="Email")
    total = fields.Float(string="Total")
    carrier = fields.Char(string="Carrier")
    currency_id = fields.Many2one('res.currency', required=True,
                                  default=lambda self: self.env.company.currency_id)
    shipping_price = fields.Float(string="Shipping Price")
    Received_date = fields.Date(string="Received Date")
    expired_date = fields.Date(string="Expired Date")
    message = fields.Char(string="Message")
    product_ids = fields.One2many('quotation.product', 'quotation_id', string="Products")
    carrier_id = fields.Many2one('delivery.carrier', string="Carrier Id")

    @api.model
    def create(self, vals):
        """Send an email when a new record is created."""
        record = super(CarrierQuotation, self).create(vals)
        try:
            if record.status == 'open':
                # Retrieve the email template
                customer_template = self.env.ref('wbl_shipping_quotation.delivery_quote_summary',
                                                 raise_if_not_found=False)
                if customer_template:
                    # Fetch the creator's email
                    user_email = record.create_uid.partner_id.email
                    admin_email = self.env.ref("base.user_admin").partner_id.email
                    if user_email and admin_email:
                        # Configure email values
                        email_values = {
                            'email_to': user_email,
                            'email_from': admin_email,  # Sender is the admin
                        }
                        # Send the email
                        customer_template.send_mail(record.id, force_send=True, email_values=email_values)
                        _logger.info(f"Delivery Quotation email sent to {user_email} for record {record.name}.")
                    else:
                        _logger.warning("User or admin email is missing. Email not sent.")
        except Exception as e:
            _logger.error(f"Failed to send email for Delivery Quotation {record.name}: {e}")
        return record

    ########For changing the state ##########
    def approve_action(self):
        """Change the status to 'sent' and send an email notification."""
        for record in self:
            record.status = 'sent'

            try:
                # Retrieve the email template
                approval_template = self.env.ref('wbl_shipping_quotation.delivery_quote_summary_approved',
                                                 raise_if_not_found=False)
                if approval_template:
                    # Fetch the creator's email
                    user_email = record.create_uid.partner_id.email
                    admin_email = self.env.ref("base.user_admin").partner_id.email
                    if user_email and admin_email:
                        # Configure email values
                        email_values = {
                            'email_to': user_email,
                            'email_from': admin_email,  # Sender is the admin
                        }
                        # Send the email
                        approval_template.send_mail(record.id, force_send=True, email_values=email_values)
                        _logger.info(f"Approval email sent to {user_email} for record {record.name}.")
                    else:
                        _logger.warning("User or admin email is missing. Approval email not sent.")
            except Exception as e:
                _logger.error(f"Failed to send approval email for Delivery Quotation {record.name}: {e}")

        return True

    #####  THIS IS CRON I HAVE USED THIS TO DELETE THE RECORD WHEN THE EXPIRATION DATE WILL PASS  #########
    @api.model
    def delete_expired_quotations(self):
        """Deletes quotations whose expired_date has passed."""
        today = datetime.today().date()  # Get today's date
        expired_quotations = self.search([('expired_date', '<', today)])

        if expired_quotations:
            # Log the expired quotations
            _logger.info(f"Deleting {len(expired_quotations)} expired quotations.")
            # Delete expired quotations
            expired_quotations.unlink()
        else:
            _logger.info("No expired quotations found.")
