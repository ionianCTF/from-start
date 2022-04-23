var login = function() {
    var payload = {
        'username': $('#login_user').val(), 
        'password': $('#login_pass').val()
    }
    $.ajax({
        type: 'POST',
        contentType: 'application/json',
        url: '/',
        dataType : 'json',
        data : JSON.stringify(payload),
        success : function(result) {
          jQuery("#clash").html(result); 
        },error : function(result){
           console.log(result);
        }
    });
};
