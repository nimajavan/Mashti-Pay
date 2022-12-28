$('#send_sms_form').submit(function (e) {
    $('#code_btn').removeClass('disabled')
    e.preventDefault();
    let phone = parseInt($('#phone_num').val())
    if (phone.length <= 11 || Number.isInteger(phone) === false) {
        swal({
            title: "نشد که بشه",
            text: "لطفا شماره موبایل معتبری وارد کنید",
            icon: "error",
            button: "متوجه شدم",
        });
    } else {
        $('#code_btn').removeClass('disabled')
        $.ajax({
            type: 'POST',
            url: "/account/send_code/",
            data: {'phone': phone},
            headers: {
                "X-Requested-With": "XMLHttpRequest",
                "X-CSRFToken": getCok("csrftoken"),
            },
            success: function (response) {
                swal({
                    title: "موفق",
                    text: response['success'],
                    icon: "success",
                    button: "متوجه شدم",
                    });
            },
        })
    }
})

function getCok(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}