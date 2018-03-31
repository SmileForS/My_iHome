# -*- coding:utf-8 -*-
from flask import Flask
from config import Config
# session在flask中的扩展包
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
import redis

app = Flask(__name__)
# 加载配置项
app.config.from_object(Config)
#　创建数据库链接对象
db = SQLAlchemy(app)
# 创建redis链接对象
redis_store = redis.StrictRedis(host=Config.REDIS_HOST,port=Config.REDIS_PORT)

# 开启csrf防护
CSRFProtect(app)
# 使用session在flask扩展实现将session数据存储在redis
Session(app)