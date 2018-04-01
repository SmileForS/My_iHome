# -*- coding:utf-8 -*-
from werkzeug.routing import BaseConverter

class RegexConverter(BaseConverter):
    """自定义路由转换器，用户匹配静态文件的路由"""
    def __init__(self,url_map,*args):
        super(RegexConverter, self).__init__(url_map)
        self.regex = args[0]

