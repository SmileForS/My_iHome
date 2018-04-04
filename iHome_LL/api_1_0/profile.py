# -*- coding:utf-8 -*-
# 个人中心
from flask import session,current_app,jsonify
from iHome_LL.models import User
from iHome_LL.api_1_0 import api
from iHome_LL.utils.response_code import RET


@api.route('/users')
def get_user_info():
    """获取用户基本信息
    0.TODO判断用户是否登录
    1.获取登录用户的id
    2.查询出登录用户的基本信息
    3.构造响应数据
    4.响应登录用户信息
    """
    # 1.获取登录用户的id
    user_id = session.get('user_id')
    # 2.查询出登录用户的基本信息
    try:
        user = User.query.get('user_id')
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg=u'查询用户信息失败')
    if not user:
        return jsonify(errno =RET.NODATA,errmsg=u'用户不存在')

    # 3.构造响应数据
    response_data = {
        'avatar_url':user.avatar_url,
        'name':user.name,
        'mobile':user.mobile,
        'user_id':user.id
    }
    # 4.响应数据
    return jsonify(errno=RET.OK,errmsg=u'OK',data = response_data)



