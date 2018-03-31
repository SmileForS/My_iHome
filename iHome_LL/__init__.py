# -*- coding:utf-8 -*-
from flask import Flask
from config import configs
# session在flask中的扩展包
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
import redis

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
    return app