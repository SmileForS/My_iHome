# -*- coding:utf-8 -*-

from . import api
from iHome_LL.models import Area,House,Facility
from flask import current_app,jsonify,request,g
from iHome_LL.utils.response_code import RET
from iHome_LL.utils.common import login_required
from iHome_LL import db

@api.route('/houses/image',methods = ["POST"])
def upload_house_image():
    """上传房屋图片"""
    pass


@api.route('/houses',methods=["POST"])
@login_required
def pub_house():
    """发布新房源
    0.判断用户是否登录
    1.接收所有参数,并判断是否缺少
    2.校验参数:price / deposit,需要用户传入数字
    3.实例化房屋模型对象，并给属性赋值
    4.保存到数据库
    5.返回响应数据
    """
    #1.接收所有参数,并判断是否缺少
    json_dict = request.json

    title = json_dict.get('title')
    price = json_dict.get('price')
    address = json_dict.get('address')
    area_id = json_dict.get('area_id')
    room_count = json_dict.get('room_count')
    acreage = json_dict.get('acreage')
    unit = json_dict.get('unit')
    capacity = json_dict.get('capacity')
    beds = json_dict.get('beds')
    deposit = json_dict.get('deposit')
    min_days = json_dict.get('min_days')
    max_days = json_dict.get('max_days')

    if not all([title, price, address, area_id, room_count, acreage, unit, capacity, beds, deposit, min_days, max_days]):
        return jsonify(errno=RET.PARAMERR,errmsg=u'参数缺失')

    #2.校验参数:price / deposit,需要用户传入数字
        # 提示：在开发中，对于像价格这样的浮点数，不要直接保存浮点数，因为有精度的问题，一般以分为单位
    try:
        price = int(float(price)*100) # 0.1元 ==> 10分
        deposit = int(float(deposit)*100)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR,errmsg=u'参数格式不正确')

    #  3.实例化房屋模型对象，并给属性赋值
    house = House()
    house.user_id = g.user_id
    house.area_id = area_id
    house.title = title
    house.price = price
    house.address = address
    house.room_count = room_count
    house.acreage = acreage
    house.unit = unit
    house.capacity = capacity
    house.beds = beds
    house.deposit = deposit
    house.min_days = min_days
    house.max_days = max_days

    # 处理房屋的设施　facilities = [2,4,6]
    facilities = json_dict.get('facility')
    # 查询出被选中的设施模型                       设施id在facilities这个列表中的所有设施模型
    house.facilities = Facility.query.filter(Facility.id.in_(facilities)).all()
    # print house.facilities
    #
    # 4.保存到数据库
    # try:
    #     db.session.add(house)
    #     db.session.commit()
    # except Exception as e:
    #     current_app.logger.error(e)
    #     db.session.rollback()
    #     return jsonify(errno=RET.DBERR,errmsg=u'发布新房源失败')

    # 5.响应结果
    return jsonify(errno=RET.OK,errmsg=u'发布新房源成功',data = {'house_id':house.id})


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