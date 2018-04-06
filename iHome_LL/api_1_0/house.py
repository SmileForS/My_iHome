# -*- coding:utf-8 -*-

from . import api
from iHome_LL.models import Area,House,Facility,HouseImage
from flask import current_app,jsonify,request,g
from iHome_LL.utils.response_code import RET
from iHome_LL.utils.common import login_required
from iHome_LL import db,constants
from iHome_LL.utils.image_storage import upload_image

@api.route('/houses/image',methods = ["POST"])
@login_required
def upload_house_image():
    """上传房屋图片
    0.判断用户是否登录       @login_required
    1.接收参数：house_id,房屋图片,并校验参数
    2.根据house_id获取房屋模型对象
    3.上传房屋图片
    4.创建house_image模型对象，存储房屋图片数据到数据库
    5.响应结果
    """
    # 1.接收参数：house_id,房屋图片,并校验参数
    try:
        image_data = request.files.get('house_image')
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR,errmsg=u'图片错误')
    house_id = request.form.get('house_id')
    if not house_id:
        return jsonify(errno=RET.PARAMERR,errmsg=u'缺少必传参数')

    # 2.根据house_id获取房屋模型对象
    try:
        house = House.query.get(house_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg=u'查询房屋信息失败')
    if not house:
        return jsonify(errno=RET.NODATA,errmsg=u'房屋不存在')
    # 3.上传房屋图片
    try:
        key =upload_image(image_data)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.THIRDERR,errmsg=u'上传图片失败')
    # 4.创建house_image模型对象，存储房屋图片数据到数据库
    house_image = HouseImage()
    house_image.house_id=house.id
    house_image.url = key
    # 保存到数据库
    try:
        db.session.add(house_image)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR,errmsg=u'保存房屋图片失败')

    # 5.响应结果:上传的图片需要立即刷新出来
    image_url = constants.QINIU_DOMIN_PREFIX + key
    return jsonify(errno=RET.OK,errmsg=u'上传房屋图片成功',data = {'image_url':image_url})


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