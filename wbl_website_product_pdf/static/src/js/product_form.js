/** @odoo-module **/
import publicWidget from "@web/legacy/js/public/public_widget";
import { jsonrpc } from '@web/core/network/rpc_service';

publicWidget.registry.DynamicPayment = publicWidget.Widget.extend({
    selector: '.js_product',
    events: {
        'click #product_pdf_view': '_onButtonClick',
        'click #selectAll': '_onSelectAll',  // Add event for 'Select All'

    },

//####### THIS BUTTON  IS FOR POPUP THE  ###########
    async _onButtonClick(ev) {
        console.log('Still working 1');

        const modal = document.getElementById('message_popup');
        if (modal) {
            $(modal).modal('show');
        } else {
            console.error('Modal not found');
        }
    },
     // Method for handling "Select All" checkbox click
    _onSelectAll(ev) {
    // Get the checked state of the "Select All" checkbox
    const selectAllChecked = $(ev.currentTarget).is(':checked');
    console.log('hello'); // For debugging to check if the function is called

    // Check or uncheck all product checkboxes
    $('.product-checkbox').each(function () {
        $(this).prop('checked', selectAllChecked); // Check or uncheck the checkbox

        const productName = $(this).data('product-id'); // Use appropriate data attribute
        if (productName) {
            console.log(`Product Name: ${productName}`); // Print the product name
        }
    });
    }
   });