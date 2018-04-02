# -*- coding:utf-8 -*-
from flask import Blueprint,current_app,make_response
from flask_wtf.csrf import generate_csrf
html_blue = Blueprint('html_blue',__name__)

@html_blue.route('/<re(".*"):file_name>')
def get_static_html(file_name):
    """获取静态文件"""
    # 需求1：http://127.0.0.1:5000/login.html
    # file_path = 'html/' + file_name
    # 需求2：http://127.0.0.1:5000/ 默认加载index.html
    if not file_name:
        file_name = 'index.html'
    # 需求3：http://127.0.0.1:5000/favicon.ico  加载title图标
    if file_name != 'favicon.ico':
        file_name = 'html/' + file_name

    # 获取response
    response = make_response(current_app.send_static_file(file_name))
    # 生成token
    token = generate_csrf()
    #　将csrf_token数据写入到cookie
    response.set_cookie('csrf_token',token)
    #send_static_file:内部用于将静态文件从静态文件夹发送到浏览器的功能
    return response

