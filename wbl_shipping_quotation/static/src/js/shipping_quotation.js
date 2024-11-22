import publicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";

publicWidget.registry.websiteSaleShippingQuotation = publicWidget.Widget.extend({
    selector: '.oe_website_sale',
    events: {
        'click #product_pdf_view': '_onSaveQuotation',
    },

    async _onSaveQuotation(ev) {
        // Capture the relevant order data (assuming it's available in the DOM or as part of the order context)
        console.log('button clicked');
        const orderData = {

        };

        // Make an RPC call to save the quotation details
        const result = await rpc('/custom/save_carrier_quotation', {
            order_data: orderData,
        });

        if (result.success) {
            window.location.href='/my/shipping/quotation'
            console.log('Quotation saved successfully');
        } else {
            console.log('Failed to save quotation');
        }
    },
});
