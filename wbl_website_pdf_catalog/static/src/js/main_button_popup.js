import publicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";

publicWidget.registry.DynamicPayment = publicWidget.Widget.extend({
    selector: '#wrapwrap',

    events: {
       'click #main_button_pdf_view': '_onButtonClick',
    },

    // Method for opening the modal popup
    _onButtonClick: function (ev) {
        console.log('button clicked');
        const modal = document.getElementById('message_popup');
        if (modal) {
            $(modal).modal('show');
        } else {
            console.error('Modal not found');
        }
    },
});
