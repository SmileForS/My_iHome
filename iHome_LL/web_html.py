# -*- coding:utf-8 -*-
from flask import Blueprint,current_app

html_blue = Blueprint('html_blue',__name__)

@html_blue.route('/<file_name>')
def get_static_html(file_name):
    """获取静态文件"""
    # 需求1：http://127.0.0.1:5000/login.html
    # 需求2：http://127.0.0.1:5000/ 默认加载index.html
    # 需求3：http://127.0.0.1:5000/favicon.ico  加载title图标
    file_path = 'html/'+file_name
    #send_static_file:内部用于将静态文件从静态文件夹发送到浏览器的功能
    return current_app.send_static_file(file_path)

