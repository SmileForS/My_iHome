# -*- coding:utf-8 -*-
import redis
from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from config import configs
from iHome_LL.utils.common import RegexConverter
import logging
from logging.handlers import RotatingFileHandler

# 创建可以被外界导入的数据库链接对象
db = SQLAlchemy()
# 创建可以被外界导入的链接到redis数据库的对象
redis_store = None

# 业务逻辑一开始就开启日志
def setupLogging(level):
    """
    如果是开发模式:development -->DEBUG
    如果是生产模式:production  -->WARN
    """
    # 设置日志的记录等级
    logging.basicConfig(level=level)  # 调试debug级
    # 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
    file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024*1024*100, backupCount=10)
    # 创建日志记录的格式                 日志等级    输入日志信息的文件名 行数    日志信息
    formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
    # 为刚创建的日志记录器设置日志记录格式
    file_log_handler.setFormatter(formatter)
    # 为全局的日志工具对象（flask app使用的）添加日志记录器
    logging.getLogger().addHandler(file_log_handler)
    # app.logger.addHandler(file_log_handler)

def get_app(config_name):
    app = Flask(__name__)
    # 调用封装的日志
    setupLogging(configs[config_name].LOGGING_LEVEL)

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

    # 需要现有路由转换器，后面html_blue才能直接匹配
    app.url_map.converters['re'] = RegexConverter
    # 注册蓝图到app中，注册蓝图的时候才导入蓝图
    from iHome_LL.api_1_0 import api
    app.register_blueprint(api)
    # 注册静态文件访问的蓝图到app中
    from iHome_LL.web_html import html_blue
    app.register_blueprint(html_blue)

    return app