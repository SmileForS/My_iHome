# -*- coding:utf-8 -*-
# 图片验证码和短信验证码
from iHome_LL import constants
from iHome_LL import redis_store
from iHome_LL.utils.captcha.captcha import captcha
from iHome_LL.utils.response_code import RET
from . import api
from flask import request,make_response,jsonify,abort,current_app
import logging
import json
import re

@api.route('/sms_code',methods=['POST'])
def send_sms_code():
    """发送短信验证码"""
    # 1.接受参数:手机号,图片验证码,uuid
    # 2.判断参数是否缺少,并且要对手机号进行校验
    # 3.获取服务器存储的图片验证码,uuid作为key
    # 4.与客户端传入的图片验证码对比
    # 5.对比成功,发送短信给用户
    # 6.响应短信发送的结果

    # 1.接受参数:手机号,图片验证码,uuid
    # data:保存请求报文里面的原始的字符串,开发文档约定,客户端发送的是json字符串
    json_str = request.data
    json_dict = json.loads(json_str)

    mobile = json_dict.get('mobile')
    imageCode_client = json_dict.get('imagecode')
    uuid = json_dict.get('uuid')

    # 2.判断参数是否缺少,并且要对手机号进行校验
    if not all([mobile,imageCode_client,uuid]):
        return jsonify(errno=RET.PARAMERR,errmsg=u'缺少参数')
    #对手机号进行校验
    if not re.match(r'^1[345678][0-9]{9}$',mobile):
        return jsonify(errno=RET.PARAMERR,errmsg=u'手机号格式错误')
    # 3.获取服务器存储的图片验证码,uuid作为key
    try:
        imageCode_server = redis_store.get('ImageCode:'+uuid)

    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg=u'查询服务器验证码失败')
    # 判断是否为空或者过期
    if not imageCode_server:
        return jsonify(errno=RET.NODATA,errmsg=u'验证码不存在')
    # 4.与客户端传入的图片验证码对比
    if imageCode_client != imageCode_server:
        return jsonify(errno=RET.DATAERR,errmsg=u'验证码输入有误')
    # TODO 5.发送短信给用户

    #6.响应短信发送的结果
    return '下一步进入发送短信的逻辑'


@api.route('/image_code')
def get_image_code():
    """提供图片验证码"""
    # 1.接受请求，获取uuid
    # 2.生成图片验证码
    # 3.使用uuid存储图片验证码内容
    # 4.返回图片验证码

    #1.获取uuid
    uuid = request.args.get('uuid')
    last_uuid = request.args.get('last_uuid')
    if not uuid:
        abort(403)
        # return jsonify(errno=RET.PARAMERR,errmsg=u'缺少参数')

    #2. 生成图片验证码,text是验证码的文字信息，image验证码的图片信息
    name,text,image= captcha.generate_captcha()
    current_app.logger.debug('图片验证码文字信息'+text)
    # 将调试信息写入logs/log
    # logging.debug('图片文字信息' + text)
    # print u'haha'


    # 3.使用uuid存储图片验证码内容
    try:
        if last_uuid:
            # 上次的uuid还在，需要在redis中删除
            redis_store.delete('ImageCode:'+last_uuid)
        # 保存本次需要记录的验证码数据
        redis_store.set('ImageCode:'+uuid,text,constants.IMAGE_CODE_REDIS_EXPIRES)
    except Exception as e:
        print e
        #将错误信息写入logs/log
        logging.error(e)
        return jsonify(errno=RET.DBERR,errmsg=u'保存验证码数据失败')
    #4 返回图片验证码
    response = make_response(image)
    response.headers['Content-Type']='image/jpg'
    return response