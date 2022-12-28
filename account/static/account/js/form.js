$(document).ready(function () {
    $('#buy-radio').on('click', function () {
        const form_shop = document.querySelector("#shop_form");
        const code = document.querySelector('#code-v');
        const active_code = document.querySelector('#a-code');
        const v_count = document.querySelector('#v-count');
        const total_price = document.querySelector('#total-price');
        form_shop.action = "/order/buy_order/";
        total_price.style.display = "block";
        code.style.display = "none";
        active_code.style.display = "none";
        v_count.style.display = "block";

    });

    $('#sell-radio').on('click', function () {
        const form_shop = document.querySelector("#shop_form");
        const code = document.querySelector('#code-v');
        const active_code = document.querySelector('#a-code');
        const v_count = document.querySelector('#v-count');
        const total_price = document.querySelector('#total-price');
        form_shop.action = "/order/sell_order/";
        code.style.display = "block";
        active_code.style.display = "block";
        v_count.style.display = "none";
        total_price.style.display = "none";

    });

    $('#v-count').on('change', function (){
        const t_num = document.querySelector('#t-num');
        const dollar_price = document.querySelector('#dollar-price').value;
        const v_count = document.querySelector('#v-count').value;

        t_num.value = dollar_price * v_count;

    });
});