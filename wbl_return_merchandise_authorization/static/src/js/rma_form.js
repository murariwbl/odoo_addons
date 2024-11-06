/** @odoo-module **/
import publicWidget from "@web/legacy/js/public/public_widget";
import { jsonrpc } from '@web/core/network/rpc_service';

publicWidget.registry.DynamicPayment = publicWidget.Widget.extend({
    selector: '#portal_sale_content',
    events: {
        'click #rma_return_button': '_onButtonClick',  // This is the single product button popup form
        'click #rma_data_save': '_onSubmitButtonClick',  // This is the single product form submit button
        'click #rma_main_return_button': '_onMainButtonClick',  //This is the main button for popup the form
        'click #rma_order_data_save': '_onClickSubmitButton',   // This button is main button form popup submit button
        'click #select_all_products': '_onSelectAllProducts',  // Add event for 'Select All'
        'click .product-checkbox': '_onProductCheckboxClick'  // Event for individual 'product' checkboxes
    },
        ////the product page popup the form ////////
    async _onButtonClick(ev) {
        console.log('Still working 1')
        const $input = $(ev.currentTarget);
        const orderLineId = $input.data('order-line');
        const orderLineId_new = $input.data('order-line-id');
        const productName = $input.data('product-name');
        const productId = $input.data('product-id');
        const unitPrice = $input.data('unit-price');
        const quantity = $input.data('quantity');

        // Populate modal form fields
        document.getElementById('orders').value = orderLineId;
        document.getElementById('product').value = productName;
//        document.getElementById('unit_price').value = unitPrice;
        document.getElementById('unit_price').value = parseFloat(unitPrice).toFixed(2);
        document.getElementById('quantity').value = quantity;
        document.getElementById('product_id').value = productId;

        const modal = document.getElementById('message_popup');
        if (modal) {
            $(modal).modal('show');
        } else {
            console.error('Modal not found');
        }

        // Fetch RMA reasons
        try {
            const response = await jsonrpc("/get_rma_reasons", { order_id: orderLineId });
            console.log(response,'===============')
            this.populateDropdown('reason', response.reason_list, 'id', 'name');
            this.populateDropdown('request_type', response.request_type_list, 'id', 'name');
        } catch (error) {
            console.error('Error fetching RMA reasons:', error);
        }
    },
        /////the product page create rma order click on submit button//////
    async _onSubmitButtonClick(ev) {
         console.log('Still working 2')
        const quantity = $("#quantity").val();
        const requestType = $("#request_type").val();
        const reason = $("#reason").val();
        const product_id = $("#product_id").val();
        const customOrderId = $("#orders").data('custom-order-id');
        const unitPrice = $("#unit_price").data('unit-price');

        try {
            const response = await jsonrpc("/save_rma_reasons", {
                order_id: customOrderId,
                product_id: product_id,
                quantity: quantity,
                reason_id: requestType,
                reason_type_id: reason,
                price: unitPrice
            });

            console.log(response);

            if (response.success === false) {
                // Show error modal
                $('#inquiry-error-modal').modal("show");

                // Hide form modal
                $("#message_popup").modal('hide');

                // Optionally set error message
                $('#rma_message_text').text(response.message);
            } else {
                // Show success modal
                $("#inquiry-success-modal").modal('show');

                // Hide form modal
                $("#message_popup").modal('hide');
            }
        } catch (error) {
            console.error('Error saving RMA reasons:', error);
        }
    },
        ////the main return button on sale order /////
    async _onMainButtonClick(ev) {
        try {
            console.log("Still Working 1")
            const $input = $(ev.currentTarget);
            const orderLineId = $input.data('order-line');
            const orderLineId_new = $input.data('order-line-id');
            const productName = $input.data('product-name');
            const unitPrice = $("#unit_price").val();

            console.log(orderLineId, orderLineId_new, productName, unitPrice);

            // Populate modal form fields
            document.getElementById('rorders').value = orderLineId;

            // Show the modal
            const modal = document.getElementById('message_popups');
            if (modal) {
                $(modal).modal('show');
            } else {
                console.error('Modal not found');
                return;  // Early exit if modal not found
            }

            // Fetch RMA reasons and populate dropdowns
            const response = await jsonrpc("/get_rma_reasons_type", { order_id: orderLineId_new });
            this.populateDropdown('rreason', response.reason_lists, 'id', 'name');
            this.populateDropdown('rrequest_type', response.request_type_lists, 'id', 'name');
            this.populateProductDropdown('rproduct', response.sale_orders);
        } catch (error) {
            console.error('Error fetching RMA reasons:', error);
        }
    },
     /////the main page create rma save button//////
    async _onClickSubmitButton(ev) {
    console.log("Still Working 2");

    // Fetch request type, reason, and custom order IDs
    const requestType = $("#rrequest_type").val();
    const reason = $("#rreason").val();
    const customOrderIds = $("#rorders").data('custom-order-ids');
    console.log('==', requestType, reason, customOrderIds);

    const selectedProducts = [];

    // Loop through all checked product checkboxes
    $('.product-checkbox:checked').each(function () {
        const productId = $(this).data('product-id');
        const unitPrice = $(this).closest('tr').find('span.unit-price').text();
        const quantity = $(this).closest('tr').find('span.product-quantity').text();

        // Add product details to the array
        selectedProducts.push({
            productId: productId,
            unitPrice: unitPrice,
            quantity: quantity
        });
    });

    // Check if no products were selected
    if (selectedProducts.length === 0) {
         $('#select-product_error-modal').modal("show");
        return;  // Exit the function to prevent form submission
    }

    // Log the collected product data for debugging
    console.log('Selected Products:', selectedProducts);

    try {
        console.log('Selected Products==:', selectedProducts);

        // Send the collected data to the backend via JSON-RPC
        const response = await jsonrpc("/save_rma_order_reasons", {
            order_id: customOrderIds,
            products: selectedProducts,  // Send the entire array of products
            reason_id: requestType,
            reason_type_id: reason,
        });

        console.log('Selected Products++:', selectedProducts);
        console.log(response);

        // Check response success and handle modals accordingly
        if (response.success === false) {
            $('#inquiry-error-modal').modal("show");
            $("#inquiry-success-modal").modal('hide');
            $('#rma_message_text').text(response.message);
        } else {
            $("#inquiry-success-modal").modal('show');
        }
    } catch (error) {
        console.error('Error saving RMA reasons:', error);
    }
},
    // Method for handling "Select All" checkbox click
    _onSelectAllProducts(ev) {
        const selectAllChecked = $(ev.currentTarget).is(':checked');

        $('.product-checkbox').each(function () {
            $(this).prop('checked', selectAllChecked);

            const productId = $(this).data('product-id');
            const unitPrice = $(this).closest('tr').find('span.unit-price').text();
            const quantity = $(this).closest('tr').find('span.product-quantity').text();

            if (selectAllChecked) {
                console.log(`Product ID: ${productId}, Unit Price: ${unitPrice}, Quantity: ${quantity}`);
            }
        });
    },
    // Method for handling individual product checkbox click
    _onProductCheckboxClick(ev) {
        const $input = $(ev.currentTarget);
        const productId = $input.data('product-id');
        const unitPrice = $input.closest('tr').find('span.unit-price').text();
        const quantity = $input.closest('tr').find('span.product-quantity').text();

        if ($input.is(':checked')) {
            console.log(`Product ID: ${productId}, Unit Price: ${unitPrice}, Quantity: ${quantity}`);
        } else {
            console.log(`Product ID: ${productId} was unchecked.`);
        }
    },

    // Helper function to populate dropdowns
    populateDropdown(dropdownId, items, valueKey, textKey) {
        const dropdown = document.getElementById(dropdownId);
        if (dropdown) {
            dropdown.innerHTML = '';
            items.forEach(item => {
                const option = document.createElement('option');
                option.value = item[valueKey];
                option.textContent = item[textKey];
                dropdown.appendChild(option);
            });
        }
    },

    // Helper function to populate product dropdown
    populateProductDropdown(dropdownId, saleOrders) {
        const productDropdown = document.getElementById(dropdownId);
        if (productDropdown) {
            productDropdown.innerHTML = '';
            saleOrders.forEach(line => {
                const option = document.createElement('option');
                option.value = line.product_id;
                option.textContent = line.product_name;
                productDropdown.appendChild(option);
            });

         // Set event listener for product selection
            productDropdown.addEventListener('change', function () {
                const selectedProductId = this.value;
                const selectedProduct = saleOrders.find(line => line.product_id == selectedProductId);

                if (!selectedProduct) {
                    document.getElementById('runit_price').value = '';
                    document.getElementById('rquantity').value = '';
                } else {
                    document.getElementById('runit_price').value = selectedProduct.price_unit;
                    document.getElementById('rquantity').value = selectedProduct.quantity;
                }
            });
        }
    },
});

export default publicWidget.registry.DynamicPayment;

