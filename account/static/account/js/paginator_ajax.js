function buy_history_ajax(page_num) {
    $.ajax({
        type: 'GET',
        url: '/account/profile/',
        data: {'page_buy': page_num},
        success: function () {
            swal({
                title: "موفق",
                text: 'success',
                icon: "success",
                button: "متوجه شدم",
            });
        }
    })
}