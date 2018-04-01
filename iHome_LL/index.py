# -*- coding:utf-8 -*-
from flask import Blueprint

# 创建蓝图
api = Blueprint('api',__name__)

# 注册路由
@api.route('/',methods=['GET','POST'])
def index():
    # 测试redis链接
    from iHome_LL import redis_store
    redis_store.set('name2','HahA')

    # 测试session：flask自带的session模块，用于存储session
    # from flask import session
    # session['name'] = 'sz_LL'


    return 'index'