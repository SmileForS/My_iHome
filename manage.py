# -*- coding:utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
class Config(object):
    """加载配置"""
    # 开启调试模式
    DEBUG = True
    # 配置mysql数据库:开发中使用真实IP
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@127.0.0.1:3306/iHome'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

app = Flask(__name__)

# 加载配置项
app.config.from_object(Config)
#　创建数据库链接对象
db = SQLAlchemy(app)


@app.route('/')
def index():
    return 'index'


if __name__ == '__main__':
    app.run(debug=True)
