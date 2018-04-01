# -*- coding:utf-8 -*-
from flask import Blueprint

# 创建蓝图
api = Blueprint('api',__name__,url_prefix='/api/1.0')

# 在这导入该蓝图定义的路由
from . import index