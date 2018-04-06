# -*- coding:utf-8 -*-

from . import api
from iHome_LL.models import Area
from flask import current_app,jsonify
from iHome_LL.utils.response_code import RET

@api.route('/areas')
def get_areas_info():
    """查询城区信息
    1.从数据库中查出所有城区的信息
    2.组织响应数据
    3.响应结果
    """
    # 1.从数据库中查出所有城区的信息
    try:
        areas = Area.query.all()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg=u'查询城区信息失败')
    # 2.组织响应数据
    areas_dict_list = []
    for area in areas:
        areas_dict_list.append(area.to_dict())

    # 3.响应结果
    return jsonify(errno=RET.OK,errmsg=u'OK',data =areas_dict_list)