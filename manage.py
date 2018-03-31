# -*- coding:utf-8 -*-
from flask import Flask

class Config(object):
    """加载配置"""
    # 开启调试模式
    DEBUG = True

app = Flask(__name__)

# 加载配置项
app.config.from_object(Config)



@app.route('/')
def index():
    return 'index'


if __name__ == '__main__':
    app.run(debug=True)
