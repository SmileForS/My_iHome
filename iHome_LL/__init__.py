# -*- coding:utf-8 -*-
import redis
from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from config import configs


# 创建可以被外界导入的数据库链接对象
db = SQLAlchemy()
# 创建可以被外界导入的链接到redis数据库的对象
redis_store = None

def get_app(config_name):
    app = Flask(__name__)
    # 加载配置项
    app.config.from_object(configs[config_name])
    #　创建数据库链接对象
    # db = SQLAlchemy(app)
    db.init_app(app)
    # 创建redis链接对象
    # 为了与上面那个空的redis关联起来，用全局声明
    global redis_store
    redis_store = redis.StrictRedis(host=configs[config_name].REDIS_HOST,port=configs[config_name].REDIS_PORT)

    # 开启csrf防护
    CSRFProtect(app)
    # 使用session在flask扩展实现将session数据存储在redis
    Session(app)
    # 注册蓝图到app中，注册蓝图的时候才导入蓝图
    from iHome_LL.api_1_0 import api
    app.register_blueprint(api)
    # 注册静态文件访问的蓝图到app中
    from iHome_LL.web_html import html_blue
    app.register_blueprint(html_blue)

    return app