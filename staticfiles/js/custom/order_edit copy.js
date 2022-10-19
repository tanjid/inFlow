let rowIdx = $('#itemTable tr').length - 1;
addedSKuList = []
function calculateGrandTotal() {
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
            const selectedSku = Object.values(mainData).filter(mainData => mainData.sku === skuValue.val());

            $(`#pp${i + 1}`).val(selectedSku[0].sell_price);

        })

        $(`#sq${i + 1}`).on('change', function () {
            let qtyValue = $(`#sq${i + 1}`).val()
            $(`#it${i + 1}`).val(parseInt($(`#pp${i + 1}`).val()) * parseInt(qtyValue));
            itemTotalCalculation()
            calculateGrandTotal()
        })





    }
}

let mainData = {}
$.ajax({
    type: "GET",
    url: '/orders/load_order_data/',
    success: function (response) {
        // const data = JSON.parse(data)
        // console.log((response))
        mainData = response.data
        // data = JSON.parse(data);
        // const priceElemetn = document.getElementById('price')

        mainData.forEach(el => {

            $("[name='sku_list']").append(new Option(el.sku, el.sku));

        })


        $('[name="sku_list"]').on('change', function (e) {

            const selectedSku = Object.values(mainData).filter(mainData => mainData.sku === this.value);
            // console.log(selectedSku[0])
            // $("[name='product-price']").val(selectedSku[0].sell_price);

        });


    },
    error: function (error) {
        console.log('error', error)
    }


})

$('#addBtn').on('click', function () {

    // Adding a row inside the tbody.
    $('#tbody').append(`<tr id="R${++rowIdx}">
    <td>
      <select name="sku_list" class="form-control sku-list-class" id="sl${rowIdx}">
        <option value="1" disabled selected>Select SKU</option>
      </select>
    </td>
    <td><input type="number" class="form-control" name="sku_qty" id="sq${rowIdx}" /></td>
    <td>
      <input type="number" class="form-control" name="product-price" autocomplete="off" id="pp${rowIdx}">
    </td>
    <td>
      <input type="number" class="form-control" name="item-total" autocomplete="off" id="it${rowIdx}">
    </td>

    <td class="text-center">
    <button class="btn btn-danger remove" 
        type="button">x</button>
    </td>
  </tr>`);

    mainData.forEach(el => {
        $(`#sl${rowIdx}`).append(new Option(el.sku, el.sku));

    })
    itemCalculation()
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


itemCalculation()
itemCalculation()
calculateGrandTotal()


$("#id_sub_total, #id_advance, #id_discount, #id_delivery_charge").on('change', function () {
    calculateGrandTotal()
})


