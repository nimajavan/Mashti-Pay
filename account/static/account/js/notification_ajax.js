function notification_read(){
    $.ajax({
        url: '/account/notification_read/',
        type: 'GET',
        success: function(res){
            console.log(res)
        }
    })
}