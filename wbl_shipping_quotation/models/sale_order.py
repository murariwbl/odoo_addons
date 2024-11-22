from odoo import api, fields, models, _
from odoo.exceptions import MissingError, ValidationError, AccessError, UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    shipping_quotation = fields.Boolean(string="Shipping Quotation", default=False)
    quotation_id = fields.Many2one("carrier.quotation")

    def _clear_cart(self):
        """Completely clear the cart (remove all products from the sales orders)"""
        if not self.order_line:
            return
        # Check if any lines are invoiced and raise an error if needed
        invoiced_lines = self.order_line.filtered(lambda line: line.qty_invoiced > 0)
        if invoiced_lines:
            raise UserError(
                _('You cannot clear the cart for orders with invoiced products!\n\n'
                  'The following lines have already been invoiced:\n\n')
                + '\n'.join(['- %s: %s x %s' % (
                    line.product_id.with_context(display_default_code=False).display_name,
                    line.qty_invoiced,
                    line.price_unit) for line in invoiced_lines])
            )
        # Unlink all non-invoiced lines
        self.order_line.unlink()
