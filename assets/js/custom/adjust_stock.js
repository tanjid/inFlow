function loadMainData() {
    // console.log("loading data from server")
    $.ajax({
        type: "GET",
        url: '/orders/load_order_data/',
        success: function (response) {
            mainData = response.data
            console.log(mainData)
            // data = JSON.parse(data);
            // const priceElemetn = document.getElementById('price')

            // $("[name='sku_list']").find('option').not(':selected').remove();
            // mainData.forEach(el => {

            //     $("[name='sku_list']").append(new Option(el.sku, el.sku));

            // })

            $('#id_sku').on('select2:select', function (e) {
                var data = e.params.data;
                console.log(data.text);
                const selectedSku = Object.values(mainData).filter(mainData => mainData.sku === data.text);
                $("#sn1").text(selectedSku[0].stock_qty);
                if (selectedSku[0].stock_qty <= 0) {
                    $("#sn1").text("Out of stock");
                    $("#sn1").css("color", "red");
                    $("#id_qty").attr({
                        "max" : 0,            
                     });
                } else {
                    $("#sn1").text(selectedSku[0].stock_qty);
                    $("#sn1").css("color", "#50cd89");
                    $("#id_qty").attr({
                        "max" : selectedSku[0].stock_qty,      
                     });
                }

                
            });

        },
        error: function (error) {
            console.log('error', error)
        }


    })
}

loadMainData()
