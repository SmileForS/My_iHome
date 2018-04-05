function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}


function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function(){
    // TODO: 查询用户的实名认证信息


    // TODO: 管理实名信息表单的提交行为
    $('#form-auth').submit(function (event) {
        event.preventDefault();
        var real_name = $('#real-name').val();
        var id_card = $('#id-card').val();
        var params = {
            'real_name':real_name,
            'id_card':id_card
        };
        if (!real_name || !id_card){
            $('.error-msg').show();
            return ;
        }
        $('.error-msg').hide();
        $.ajax({
            url:'/api/1.0/users/auth',
            type:'post',
            data:JSON.stringify(params),
            contentType:'application/json',
            headers:{'X-CSRFToken':getCookie('csrf_token')},
            success:function (response) {
                if (response.errno=='0'){
                    showSuccessMsg();
                    //成功之后还要将输入框设为不可交互
                    $('#real-name').attr('disabled',true);
                    $('#id-card').attr('disabled',true);
                    //将保存按钮隐藏
                    $('.btn-success').hide();

                }else {
                    alert(response.errmsg);
                }

            }

        })
    })
});