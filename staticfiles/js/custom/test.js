
let rowIdx = 1;
function calculateGrandTotal() {
    if (isNaN($('#id_sub_total').val())) {
        $('#id_sub_total').val(0)
    }

    $('#id_grand_total').val(parseInt($('#id_sub_total').val()) + parseInt($('#id_delivery_charge').val()) - parseInt($('#id_advance').val()) - parseInt($('#id_discount').val()))
}

function itemTotalCalculation() {
    let itemTotalSum = 0
    for (let i = 0; i < rowIdx; i++) {
        itemTotalSum += parseInt($(`#it${i + 1}`).val())

    }
    $('#id_sub_total').val(itemTotalSum);
}


function itemCalculation() {
    for (let i = 0; i < rowIdx; i++) {
        const skuValue = $(`#sl${i + 1}`);
        $(`#sl${i + 1}`).on('change', function () {
            let qtyValue = $(`#sq${i + 1}`).val()
            const selectedSku = Object.values(mainData).filter(mainData => mainData.sku === skuValue.val());

            $(`#pp${i + 1}`).val(selectedSku[0].sell_price);

            if (selectedSku[0].stock_qty <= 0) {
                $(`#sn${i + 1}`).text("Out of stock");
                $(`#sn${i + 1}`).css("color", "red");
            } else {
                $(`#sn${i + 1}`).text(selectedSku[0].stock_qty);
                $(`#sn${i + 1}`).css("color", "#50cd89");
            }
            $(`#sq${i + 1}`).attr({
                "max": selectedSku[0].stock_qty,
            })

            $(`#it${i + 1}`).val(parseInt($(`#pp${i + 1}`).val()) * parseInt(qtyValue));
            itemTotalCalculation()
            $('#id_grand_total').val(parseInt($('#id_sub_total').val()) + parseInt($('#id_delivery_charge').val()) - parseInt($('#id_advance').val()) - parseInt($('#id_discount').val()))


        })

        $(`#sl${i + 1}`).select2();



        // $(`#sq${i + 1}`).on('click', function () {
        //     let qtyValue = $(`#sq${i + 1}`).val()
        //     $(`#it${i + 1}`).val(parseInt($(`#pp${i + 1}`).val()) * parseInt(qtyValue));
        //     itemTotalCalculation()
        //     calculateGrandTotal()
        // })

        $(`#sq${i + 1}`).on('change', function () {
            let qtyValue = $(`#sq${i + 1}`).val()
            $(`#it${i + 1}`).val(parseInt($(`#pp${i + 1}`).val()) * parseInt(qtyValue));
            itemTotalCalculation()
            calculateGrandTotal()
        })







    }
}


let mainData = {}

function loadMainData() {
    // console.log("loading data from server")
    $.ajax({
        type: "GET",
        url: '/orders/load_order_data/',
        success: function (response) {
            mainData = response.data
            // console.log(mainData)
            // data = JSON.parse(data);
            // const priceElemetn = document.getElementById('price')

            $("[name='sku_list']").find('option').not(':selected').remove();
            mainData.forEach(el => {

                $("[name='sku_list']").append(new Option(el.sku, el.sku));

            })

        },
        error: function (error) {
            console.log('error', error)
        }


    })
}

loadMainData()
$('#addBtn').on('click', function () {

    // Adding a row inside the tbody.
    $('#tbody').append(`<tr id="R${++rowIdx}">
    <td>
      <select name="sku_list" class="form-control sku-list-class" id="sl${rowIdx}" data-control="select2">
        <option value="1" disabled selected>Select SKU</option>
      </select>
      <span id = "sn${rowIdx}"style="width: 100%;
      margin-top: 0.5rem;
      font-size: 0.925rem;
      color: #50cd89;"></span>
    </td>
    <td><input type="number" class="form-control" name="sku_qty" id="sq${rowIdx}" value="1" value="1" /></td>
    <td>
      <input type="number" class="form-control" name="product-price" autocomplete="off" id="pp${rowIdx}" value="0" readonly>
    </td>
    <td>
      <input type="number" class="form-control" name="item-total" autocomplete="off" id="it${rowIdx}" value="0" readonly>
    </td>

    <td class="text-center">
    <button class="btn btn-danger remove" 
        type="button">x</button>
    </td>
  </tr>`);

    mainData.forEach(el => {
        $(`#sl${rowIdx}`).append(new Option(el.sku, el.sku));

    })

    $("[name='sku_list']").on("change", function () {
        itemCalculation()
        itemTotalCalculation()
        calculateGrandTotal()

    })
    itemCalculation()
    itemTotalCalculation()
    calculateGrandTotal()

});

$('#tbody').on('click', '.remove', function () {

    // Getting all the rows next to the 
    // row containing the clicked button
    var child = $(this).closest('tr').nextAll();

    // Iterating across all the rows 
    // obtained to change the index
    child.each(function () {
        // Getting <tr> id.
        var id = $(this).attr('id');


        // Gets the row number from <tr> id.
        var dig = parseInt(id.substring(1));

        // Modifying row id.
        $(this).attr('id', `R${dig - 1}`);

        $(`#sl${dig}`).attr('id', `sl${dig - 1}`)
        $(`#sq${dig}`).attr('id', `sq${dig - 1}`)
        $(`#pp${dig}`).attr('id', `pp${dig - 1}`)
        $(`#it${dig}`).attr('id', `it${dig - 1}`)

    });


    // Removing the current row.
    $(this).closest('tr').remove();

    // Decreasing the total number of rows by 1.
    rowIdx--;

    // Calculating Items Again
    itemCalculation()
    itemTotalCalculation()
    calculateGrandTotal()



});

$("#id_sub_total, #id_advance, #id_discount, #id_delivery_charge").on('change', function () {
    calculateGrandTotal()
})

$("[name='sku_list']").on("change", function () {
    itemCalculation()
    itemTotalCalculation()
    calculateGrandTotal()
    loadMainData()
})


itemCalculation()



const findDuplicates = (arr) => {
    let sorted_arr = arr.slice().sort();
    let results = [];
    for (let i = 0; i < sorted_arr.length - 1; i++) {
        if (sorted_arr[i + 1] == sorted_arr[i]) {
            results.push(sorted_arr[i]);
        }
    }
    if (results.length > 0) {
        return true
    }

    return false
}


$("form").on("submit", function (event) {
    itval = $('[name="item-total"]')
    sku_list = $('[name="sku_list"]')
    skList = []
    itemTotal = []
    $.each(itval, function (key, value) {
        itemTotal.push(value.value)
    });
    $.each(sku_list, function (key, value) {
        skList.push(value.value)
    });

    if (findDuplicates(skList)) {
        alert("There are Duplicate SKUS")
        $('#submit-btn').prop('disabled', false);
        return false
    }

    if (itemTotal.includes("0")) {
        alert("Item Total Have a Zero Value")
        $('#submit-btn').prop('disabled', false);

        return false
    }
    itemCalculation()

})

// $('#id_delivery_method option:contains(---------)').text("Select Delivery Method")


// Make the DIV element draggable:
var element = document.querySelector('#kt_modal_3');
dragElement(element);

function dragElement(elmnt) {
    var pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;
    if (elmnt.querySelector('.modal-content')) {
        // if present, the header is where you move the DIV from:
        elmnt.querySelector('.modal-content').onmousedown = dragMouseDown;
    } else {
        // otherwise, move the DIV from anywhere inside the DIV:
        elmnt.onmousedown = dragMouseDown;
    }

    function dragMouseDown(e) {
        e = e || window.event;
        e.preventDefault();
        // get the mouse cursor position at startup:
        pos3 = e.clientX;
        pos4 = e.clientY;
        document.onmouseup = closeDragElement;
        // call a function whenever the cursor moves:
        document.onmousemove = elementDrag;
    }

    function elementDrag(e) {
        e = e || window.event;
        e.preventDefault();
        // calculate the new cursor position:
        pos1 = pos3 - e.clientX;
        pos2 = pos4 - e.clientY;
        pos3 = e.clientX;
        pos4 = e.clientY;
        // set the element's new position:
        elmnt.style.top = (elmnt.offsetTop - pos2) + "px";
        elmnt.style.left = (elmnt.offsetLeft - pos1) + "px";
    }

    function closeDragElement() {
        // stop moving when mouse button is released:
        document.onmouseup = null;
        document.onmousemove = null;
    }
}

$("#id_number").on("change", function (elmnt) {
    number = $("#id_number").val()
    $(".user_data-btn").hide();
    $("#user_data").hide()
    if (number.length === 11) {
        $.ajax({
            type: "GET",
            url: `/orders/load_mobile_data/${number}`,
            success: function (response) {
                customerData = response.data
                console.log(customerData)

                if (jQuery.isEmptyObject(customerData)) {
                    $(".user_data-btn").hide();
                    $("#user_data").hide()

                } else {
                    $("#id_name").val(customerData.name)
                    $("#id_delivery_method").val(customerData.delivery_method)
                    $("#id_address").val(customerData.address)
                    $("#id_order_note").val(customerData.note)

                    if (customerData.Initial > 0) {
                        $("#initial_order").show()
                        $("#user_data").show()
                        $("#initial_order").text(`Ini: ${customerData.Initial}`)
                    }

                    if (customerData.Printed > 0) {
                        $("#printed_order").show()
                        $("#user_data").show()
                        $("#printed_order").text(`Pri: ${customerData.Printed}`)
                    }

                    if (customerData.Shipping > 0) {
                        $("#shipping_order").show()
                        $("#user_data").show()
                        $("#shipping_order").text(`Shi: ${customerData.Shipping}`)
                    }

                    if (customerData.Complete > 0) {
                        $("#complete_order").show()
                        $("#user_data").show()
                        $("#complete_order").text(`Comp: ${customerData.Complete}`)
                    }
                    if (customerData.Return > 0) {
                        $("#return_order").show()
                        $("#user_data").show()
                        $("#return_order").text(`Ret: ${customerData.Return}`)
                    }
                    if (customerData.Exchange > 0) {
                        $("#exchange_order").show()
                        $("#user_data").show()
                        $("#exchange_order").text(`Exc: ${customerData.Exchange}`)
                    }
                }
            },
            error: function (error) {
                console.log('error', error)
            }
        })
    } else {
        $("#initial_order").hide()
    }

})