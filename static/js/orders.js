window.onload = () => {
    let _quantity, _price, orderitem_num, delta_quantity, orderitem_quantity, delta_cost;
    let quantity_arr = [];
    let price_arr = [];

    let total_forms = parseInt($("input[name=orderitems-TOTAL_FORMS]").val());
    console.log(total_forms);

    let order_total_quantity = parseInt($(".order_total_quantity").text()) || 0;
    let order_total_price = parseFloat($(".order_total_cost").text().replace(",", ".")) || 0;

    function orderSummaryUpdate(orderitem_price, delta_quantity) {
        delta_cost = orderitem_price * delta_quantity;
        order_total_price = Number((order_total_price + delta_cost).toFixed(2));

        order_total_quantity = order_total_quantity + delta_quantity;

        $(".order_total_quantity").html(order_total_quantity.toString());
        $(".order_total_cost").html(order_total_price.toFixed(2).toString().replace(".", ","));
    }

    function deleteOrderItem(row) {
        let target_name = row[0].querySelector("input[type='number']").name;
        orderitem_num = parseInt(target_name.replace("orderitems-", "").replace("-quantity", ""));
        delta_quantity = -quantity_arr[orderitem_num];
        orderSummaryUpdate(price_arr[orderitem_num], delta_quantity);
    }

    for (let i = 0; i < total_forms; i++) {
        _quantity = parseInt($(`input[name=orderitems-${i}-quantity]`).val());
        _price = parseFloat($(`.orderitems-${i}-price`).text().replace(",", "."));

        quantity_arr[i] = _quantity;
        if (_price) {
            price_arr[i] = _price;
        } else {
            price_arr[i] = 0;
        }
        console.log(quantity_arr);
        console.info("QUANTITY_ARR: ", quantity_arr);
        console.log(price_arr);
    }

    $(".order_form")
        .on("click", "input[type=number]", () => {
            let target = event.target;
            orderitem_num = parseInt(target.name.replace("orderitems-", "").replace("-quantity", ""));
            if (price_arr[orderitem_num]) {
                orderitem_quantity = parseInt(target.value);
                delta_quantity = orderitem_quantity - quantity_arr[orderitem_num];
                quantity_arr[orderitem_num] = orderitem_quantity;
                orderSummaryUpdate(price_arr[orderitem_num], delta_quantity);
            }
        })
        .on("click", "input[type=checkbox]", () => {
            let target = event.target;
            orderitem_num = parseInt(target.name.replace("orderitems-", "").replace("-quantity", ""));
            if (target.checked) {
                delta_quantity = -quantity_arr[orderitem_num];
            } else {
                delta_quantity = quantity_arr[orderitem_num];
            }
            orderSummaryUpdate(price_arr[orderitem_num], delta_quantity);
        });

    $(".formset_row").formset({
        addText: "Добавить продукт",
        deleteText: "Удалить",
        prefix: "orderitems",
        removed: deleteOrderItem
    });

    $(".order_form select").change(function () {
        let target = event.target;
        console.log(target);
    });

};
