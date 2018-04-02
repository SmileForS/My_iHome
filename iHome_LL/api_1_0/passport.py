# -*- coding:utf-8 -*-
# 实现注册和登陆

from flask import request,json,jsonify,current_app
from iHome_LL import redis_store,db
from iHome_LL.utils.response_code import RET
from . import api
from iHome_LL.models import User



@api.route('/users',methods=["POST"])
def register():
    """
    实现注册
    1.获取请求参数：手机号，短信验证码，密码
    2.判断参数是否缺少
    3.获取服务器的短信验证码
    4.与客户端的短信验证码对比
    5.如果一致，创建User模型类对象
    6.保存注册数据到数据库
    7.响应结果
    :return:
    """
    # 1.获取请求参数：手机号，短信验证码，密码
    # 方法1
    # json_str = request.data
    # json_dict = json.loads(json_str)
    #方法2
    # json_dict = request.get_json()
    # 方法3
    json_dict =request.json

    mobile = json_dict.get('mobile')
    sms_code_client = json_dict.get('sms_code')
    password = json_dict.get('password')

    # 2.判断参数是否缺少
    if not all([mobile,sms_code_client,password]):
        return jsonify(errno=RET.PARAMERR,errmsg=u'缺少参数')
    # 3.获取服务器的短信验证码
    try:
        sms_code_server = redis_store.get('Mobile:'+mobile)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg=u'查询短信验证码失败')
    #　判断数据是否为空
    if not sms_code_server:
        return jsonify(errno=RET.NODATA,errmsg=u'短信验证码不存在')

    #4.与客户端的短信验证码对比
    if sms_code_server != sms_code_client:
        return jsonify(errno=RET.DATAERR,errmsg=u'短信验证码输入有误')
    # 5.如果一致，创建User模型类对象
    user = User()
    # 注册时，默认手机号就是用户名，如果后面需要更换用户名，也是提供的有接口和界面
    user.name = mobile
    user.mobile=mobile
    # 密码需要加密后才能存储：目前是明文存储
    # user.password_hash = password
    # 加密存储
    user.password = password
    # 6.保存注册数据到数据库
    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR,errmsg=u'注册数据保存失败')
    # 7.响应结果
    return jsonify(errno=RET.OK,errmsg=u'注册成功')