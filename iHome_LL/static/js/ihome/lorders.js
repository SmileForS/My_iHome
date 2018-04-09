//模态框居中的控制
function centerModals(){
    $('.modal').each(function(i){   //遍历每一个模态框
        var $clone = $(this).clone().css('display', 'block').appendTo('body');    
        var top = Math.round(($clone.height() - $clone.find('.modal-content').height()) / 2);
        top = top > 0 ? top : 0;
        $clone.remove();
        $(this).find('.modal-content').css("margin-top", top-30);  //修正原先已经有的30个像素
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function(){
    $('.modal').on('show.bs.modal', centerModals);      //当模态框出现的时候
    $(window).on('resize', centerModals);
    // TODO: 查询房东的订单
    $.get('/api/1.0/orders?role=landlord',function (response) {
        if (response.errno =='0'){
            //渲染页面内容
            var html = template('orders-list-tmpl',{'orders':response.data});
            $('.orders-list').html(html);
            // TODO: 查询成功之后需要设置接单处理
            $(".order-accept").on("click", function(){
                var orderId = $(this).parents("li").attr("order-id");
                $(".modal-accept").attr("order-id", orderId);
            });
            //给确定接单的标签添加点击事件
            $('.modal-accept').on('click',function () {
                //获取要接单的id
                var orderId = $('.modal-accept').attr('order-id');
                //发送ajax请求
                $.ajax({
                    url:'/api/1.0/orders/'+orderId+'?action=accept',
                    type:'put',
                    headers:{'X-CSRFToken':getCookie('csrf_token')},
                    success:function (response) {
                        if (response.errno=='0'){
                            //1.设置订单状态的html
                            $('.order-content>div.order-text>ul li:eq(4)>span').html('已接单');
                            // $(".orders-list>li[order-id="+ orderId +"]>div.order-content>div.order-text>ul li:eq(4)>span").html("已接单");
                            //2.隐藏接单和拒单操作按钮
                            // $('.order-operate').hide();  # 这个会将该订单页面所有的接单和拒单操作按钮都隐藏
                            // 因为是列表形式存在,所以需要确定要隐藏的是哪个订单的按钮,哪个<li>标签的按钮
                            $("ul.orders-list>li[order-id="+ orderId +"]>div.order-title>div.order-operate").hide();
                            //3.隐藏弹框
                            $('#accept-modal').modal('hide');
                        }else if(response.errno =='4101'){
                            location.href = '/'
                        }else {
                            alert(response.errmsg);
                        }
                    }
                })
            });
            // TODO: 查询成功之后需要设置拒单的处理
            $(".order-reject").on("click", function(){
                var orderId = $(this).parents("li").attr("order-id");
                $(".modal-reject").attr("order-id", orderId);
                });
                 //给确定拒单的标签添加点击事件
                $('.modal-reject').on('click',function () {
                //获取要接单的id
                    var orderId = $('.modal-reject').attr('order-id');
                //获取拒单理由
                    var reason = $('#reject-reason').val();
                    if(!reason){
                        alert('请输入拒单理由');
                        return;
                    }
                    var params = {
                        'reason':reason
                    };
                //发送ajax请求
                    $.ajax({
                        url:'/api/1.0/orders/'+orderId +'?action=reject',
                        type:'put',
                        data:JSON.stringify(params),
                        contentType:'application/json',
                        headers:{'X-CSRFToken':getCookie('csrf_token')},
                        success:function (response) {
                            if (response.errno=='0'){
                                //1.设置订单状态的html
                                // $('.order-content>div.order-text>ul li:eq(4)>span').html('已接单');
                                $(".orders-list>li[order-id="+ orderId +"]>div.order-content>div.order-text>ul li:eq(4)>span").html("已拒单");
                                //2.隐藏接单和拒单操作按钮
                                // $('.order-operate').hide();  # 这个会将该订单页面所有的接单和拒单操作按钮都隐藏
                                // 因为是列表形式存在,所以需要确定要隐藏的是哪个订单的按钮,哪个<li>标签的按钮
                                $("ul.orders-list>li[order-id="+ orderId +"]>div.order-title>div.order-operate").hide();
                                //3.隐藏弹框
                                $('#reject-modal').modal('hide');
                            }else if(response.errno =='4101'){
                                location.href = '/'
                            }else {
                                alert(response.errmsg);
                            }
                        }
                    });
            });


        }else if (response.errno =='4101'){
            location.href = '/';
        }else{
            alert(response.errmsg);
        }
    });


});
