# -*- coding:utf-8 -*-

from functools import wraps
from flask import session, jsonify,g
from werkzeug.routing import BaseConverter
from iHome_LL.utils.response_code import RET


class RegexConverter(BaseConverter):
    """自定义路由转换器，用户匹配静态文件的路由"""
    def __init__(self,url_map,*args):
        super(RegexConverter, self).__init__(url_map)
        self.regex = args[0]

def login_required(view_func):
    """校验用户是否是登录用户"""
    # 装饰器装饰一个函数时，会修改该函数的__name__属性
    # 如果希望装饰器装饰之后的函数，依然保留原始的名字和说明文档,就需要使用wraps装饰器，装饰内存函数
    @wraps(view_func)
    def wrapper(*args,**kwargs):
        # 获取user_id
        user_id = session.get('user_id')
        if not user_id:
            return jsonify(errno=RET.SESSIONERR,errmsg=u'用户未登录')
        else:
            # 表示用户已经登录,使用g变量保存住user_id
            g.user_id = user_id
            return view_func(*args,**kwargs)
    return wrapper
