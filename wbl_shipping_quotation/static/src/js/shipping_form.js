import publicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";

publicWidget.registry.websiteSaleDeliveryTimeSlot = publicWidget.Widget.extend({
    selector: '.oe_website_sale',
    events: {
        'click input[name=o_delivery_radio]': '_onCarrierClick',
    },

    start() {
        this._super.apply(this, arguments);
        // Check if a delivery radio button is already checked on page load
        const checkedDeliveryRadio = document.querySelector('input[name=o_delivery_radio]:checked');
        if (checkedDeliveryRadio) {
            this._onCarrierClick({ currentTarget: checkedDeliveryRadio });
        }
    },

    async _onCarrierClick(ev) {
        const delivery_id = ev.currentTarget.dataset.dmId;
        const result = await rpc('/custom/get_delivery_carrier', {
            'dm_id': delivery_id,
        });

         // Update the shipping price display
        const shippingPriceDiv = document.getElementById('shipping_price');
          console.log(shippingPriceDiv);
            if (shippingPriceDiv && result.shipping_price) {
                shippingPriceDiv.textContent = `Shipping Price: ${result.shipping_price.toFixed(2)}`;
                shippingPriceDiv.style.display = 'block';
                console.log('hello');
            } else if (shippingPriceDiv) {
                shippingPriceDiv.style.display = 'none';
            }

        // Toggle the message box display
        const messageBox = document.getElementById('require_message_box');
        const textMessage = document.getElementById('text_message');
        const continueButton = document.querySelector('a[name="website_sale_main_button"]');

        // Handle the visibility of the message box  and text message
        if (result.require_message_box && result.enable_quotation && result.shipping_quotation === false) {
            messageBox.style.display = 'block';
            textMessage.setAttribute('required', 'required');  // Make text area required
        } else {
            messageBox.style.display = 'none';
            textMessage.removeAttribute('required');  // Remove required attribute
        }

        // Handle the visibility of the continue button based on enable_quotation
        if (result.enable_quotation && result.shipping_quotation === false) {
            continueButton.style.display = 'none';
        } else {
            continueButton.style.display = 'block';
        }

        // Show custom message if message_show is enabled
        const customMessageDiv = document.getElementById('custom_message');
        const button = document.getElementById('product_pdf_view');

        if (result.message_show && result.custom_message && result.enable_quotation && result.shipping_quotation === false ) {
            console.log('if')
            customMessageDiv.textContent = result.custom_message;
            customMessageDiv.style.display = 'block';
        } else {
            console.log('else')
            customMessageDiv.style.display = 'none';

        }

         // Set button name, and show/hide button based on `enable_quotation`

        if (result.enable_quotation && result.shipping_quotation === false) {
            button.textContent = result.button_name ? result.button_name.toUpperCase() : 'GET BACK TO ME WITH SHIPPING PRICE';
            button.style.display = 'block';  // Show the button
        } else {
            button.style.display = 'none';  // Hide the button if enable_quotation is false
        }
    },
});
