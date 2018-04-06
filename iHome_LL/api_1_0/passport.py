# -*- coding:utf-8 -*-
# 实现注册和登陆
import re

from flask import request,json,jsonify,current_app,session
from iHome_LL import redis_store,db
from iHome_LL.utils.common import login_required
from iHome_LL.utils.response_code import RET
from . import api
from iHome_LL.models import User

@api.route('/sessions')
def check_login():
    """判断用户是否登录
    提示:该接口是用于前端在渲染界面时判断使用的根据不同的登陆状态,展示不同的界面
    """
    user_id = session.get('user_id')
    name = session.get('name')
    return jsonify(errno=RET.OK,errmsg=u'OK',data={'user_id':user_id,'name':name})

@api.route('/sessions',methods=['DELETE'])
@login_required
def logout():
    """退出登录接口"""
    #1.清理session数据
    session.pop('user_id')
    session.pop('name')
    session.pop('mobile')

    return jsonify(errno=RET.OK,errmsg=u'退出登录成功')

@api.route('/sessions',methods=['POST'])
def login():
    """登录验证
    1.获取参数:手机号，密码
    2.校验参数
    3.根据mobile 查询到指定用户
    4.校验密码是否正确
    5.把当前用户的登录信息写入sessions中
    6.响应结果
    """

    # 1.获取参数:手机号，密码
    json_dict = request.json
    mobile = json_dict.get('mobile')
    password = json_dict.get('password')
    # 2.校验参数
    if not all([mobile,password]):
        return jsonify(errno=RET.PARAMERR,errmsg=u'缺少参数')
    # 校验手机号
    if not re.match(r'^1[345678][0-9]{9}$',mobile):
        print
        return jsonify(errno=RET.PARAMERR,errmsg=u'手机号格式不正确')
    # 3.根据mobile 查询到指定用户
    try:
        user = User.query.filter(User.mobile==mobile).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg=u'查询用户失败')
    if not user:
        return jsonify(errno=RET.NODATA,errmsg=u'用户名或密码错误')
    #4.校验密码是否正确
    if not user.check_password(password):
        return jsonify(errno=RET.PWDERR,errmsg=u'用户名或密码错误')
    #5.把当前用户的登录信息写入session中
    session['user_id'] = user.id
    session['name'] = user.name
    session['mobile'] = user.mobile
    return jsonify(errno=RET.OK,errmsg=u'登录成功')

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
    # 1.获取请求参数：手机号，短信验证码，密码ss
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
    # 判断用户名是否已经被注册
    if User.query.filter(User.mobile==mobile).first():
        return jsonify(errno=RET.DATAEXIST,errmsg=u'用户已注册')

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
    # 把当前用户的登录信息写入sessions中
    session['user_id'] = user.id
    session['name'] = user.name
    session['mobile'] = user.mobile
    # 7.响应结果
    return jsonify(errno=RET.OK,errmsg=u'注册成功')