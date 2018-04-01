# -*- coding:utf-8 -*-
# 图片验证码和短信验证码
from iHome_LL import constants
from iHome_LL import redis_store
from iHome_LL.utils.captcha.captcha import captcha
from iHome_LL.utils.response_code import RET
from . import api
from flask import request,make_response,jsonify,abort



@api.route('/image_code')
def get_image_code():
    """提供图片验证码"""
    # 1.接受请求，获取uuid
    # 2.生成图片验证码
    # 3.使用uuid存储图片验证码内容
    # 4.返回图片验证码

    # 生成图片验证码,text是验证码的文字信息，image验证码的图片信息
    name,text,image= captcha.generate_captcha()

    # 返回图片验证码
    return image