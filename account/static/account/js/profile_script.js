$(document).ready(function () {

    const voucher_div = document.querySelector('#voucher-wallet-div')
    const ticket_form_div = document.querySelector('#ticket-form-div')
    const buy_sel_his_div = document.querySelector('#buy-sell-history')
    const sms_modal = document.querySelector('#sms-modal')
    const dashboard = document.querySelector('#d-dashboard')
    const form_buy_sell = document.querySelector('#form-buy-sell')
    const ticket_show_div = document.querySelector('#ticket-show-div')
    const profile_avatar = $('#profile_avatar')
    const nav_bar_close_btn = $('#nav-bar-close-btn')

    $('#sidebar').on('hide.bs.collapse', function (e) {
        if (e.target == this) {
            $('#main-content').removeClass('col-lg-10');
            $('#sidebar').removeClass('d-xl-flex');
        }
    })
    $('#sidebar').on('show.bs.collapse', function (e) {
        if (e.target == this) {
            $('#main-content').addClass('col-lg-10');
            $('#sidebar').addClass('d-xl-flex');
        }
    })
    $('#btnradio1').on('click', function (e) {
        $('#ehraz').removeClass('show');
        $('#mobile').removeClass('show');
        profile_avatar.removeClass('text-secondary text-success text-danger')
        profile_avatar.addClass('text-secondary')

    })
    $('#btnradio3').on('click', function (e) {
        $('#account-inf').removeClass('show');
        $('#mobile').removeClass('show');
        profile_avatar.removeClass('text-secondary text-success text-danger')
        profile_avatar.addClass('text-success')

    })
    $('#btnradio2').on('click', function (e) {
        $('#ehraz').removeClass('show');
        $('#account-inf').removeClass('show');
        profile_avatar.removeClass('text-secondary text-success text-danger')
        profile_avatar.addClass('text-danger')
    })
    $('#buy-1').on('click', function (e) {
        $('#sell-history').removeClass('show');

    })
    $('#sell-1').on('click', function (e) {
        $('#buy-history').removeClass('show');

    })
    $('#files1').on('change', function () {
        $('#id-card-form').submit();
    });
    $('#files2').on('change', function () {
        $('#bank-card-form').submit();
    });
    $('#profile_img').on('change', function (){
        $('#profile_img_from').submit();
    })


    const t_btns = document.querySelectorAll('#send-ticket');
    t_btns.forEach(t_btn => t_btn.addEventListener('click', function () {
        ticket_form_div.style.display = 'block'
        voucher_div.style.display = 'none'
        buy_sel_his_div.style.display = 'none'
        dashboard.style.display = 'none'
        form_buy_sell.style.display = 'none'
        ticket_show_div.style.display = 'block'
        nav_bar_close_btn.click()


    }))

    const buy_btns = document.querySelectorAll('#buy-his')
    buy_btns.forEach(byu_btn => byu_btn.addEventListener('click', function () {
        buy_sel_his_div.style.display = 'block'
        voucher_div.style.display = 'none'
        ticket_form_div.style.display = 'none'
        dashboard.style.display = 'none'
        form_buy_sell.style.display = 'none'
        ticket_show_div.style.display = 'none'
        nav_bar_close_btn.click()
    }))

    const sell_btns = document.querySelectorAll('#sell-his')
    sell_btns.forEach(sell_btn => sell_btn.addEventListener('click', function () {
        buy_sel_his_div.style.display = 'block'
        voucher_div.style.display = 'none'
        ticket_form_div.style.display = 'none'
        dashboard.style.display = 'none'
        form_buy_sell.style.display = 'none'
        ticket_show_div.style.display = 'none'
        nav_bar_close_btn.click()
    }))

    $('#sell-his').on('click', function (s) {
        buy_sel_his_div.style.display = 'block'
        voucher_div.style.display = 'none'
        ticket_form_div.style.display = 'none'
        dashboard.style.display = 'none'
        form_buy_sell.style.display = 'none'
        ticket_show_div.style.display = 'none'
        nav_bar_close_btn.click()
    })

    const wallet_btns = document.querySelectorAll('#wallet-btn')
    wallet_btns.forEach(wallet_btn => wallet_btn.addEventListener('click', function () {
        voucher_div.style.display = 'block'
        buy_sel_his_div.style.display = 'none'
        ticket_form_div.style.display = 'none'
        dashboard.style.display = 'none'
        form_buy_sell.style.display = 'none'
        ticket_show_div.style.display = 'none'
        nav_bar_close_btn.click()
    }))

    const buy_sell_btn = document.querySelectorAll('#buysell-l')
    buy_sell_btn.forEach(btn => btn.addEventListener('click', function () {
        voucher_div.style.display = 'none'
        buy_sel_his_div.style.display = 'none'
        ticket_form_div.style.display = 'none'
        dashboard.style.display = 'none'
        form_buy_sell.style.display = 'block'
        ticket_show_div.style.display = 'none'
        nav_bar_close_btn.click()
    }))

    $('#send-sms-btn').on('click', function () {
        $('#sms-modal').addClass('show')
        sms_modal.style.display = 'block'
    })

    $('#close-modal-btn').on('click', function () {
        $('#sms-modal').removeClass('show')
        sms_modal.style.display = 'none'
    })

    $('#profile-update-btn').on('click', function () {
        const name = $('#name-e').val();
        const lastname = $('#lastname-e').val();
        const card = $('#card-e').val();
        const shaba = $('#shaba-e').val();

        if (name !== "" & lastname !== "" & card !== "" && shaba !== "") {
            $('#user-profile-update-form').submit();
        } else {
            swal({
                title: "ناموفق",
                text: 'لطفا همه فیلد ها را کامل کنید',
                icon: "error",
                button: "متوجه شدم",
            });
        }
    })

});

