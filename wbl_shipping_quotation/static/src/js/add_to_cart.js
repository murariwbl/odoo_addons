import publicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";

publicWidget.registry.websiteSaleAddToCart = publicWidget.Widget.extend({
    selector: '.oe_website_sale',
    events: {
        'click #wbl_add_to_cart': '_onClickCart',
    },

    start() {
        this._super.apply(this, arguments);
    },

    async _onClickCart(ev) {
     console.log('hello')
    },
});
