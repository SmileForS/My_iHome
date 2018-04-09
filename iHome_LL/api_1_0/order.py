# -*- coding:utf-8 -*-
from . import api
from iHome_LL.utils.common import login_required
from flask import request,jsonify,current_app,g
from iHome_LL.utils.response_code import RET
import datetime
from iHome_LL.models import House,Order
from iHome_LL import db

@api.route('/orders/<int:order_id>',methods=['PUT'])
@login_required
def set_order_status(order_id):
    """
    确认订单
    0.判断是否登录
    1.查询order_id对应的订单信息
    2.判断当前登录用户是不是该订单id对应的订单的房屋的房东
    3.修改订单的status属性为'已接单'
    4.更新数据到数据库
    5.响应结果
    :param order_id:
    :return:
    """
    # 1.查询order_id对应的订单信息
    try:
        order = Order.query.get(order_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg=u'查询订单信息失败')
    if not order:
        return jsonify(errno=RET.NODATA,errmsg=u'订单不存在')
    #2.判断当前登录用户是不是该订单id对应的订单的房屋的房东
    # login_user_id = g.user_id
    # landlord_user_id = order.house.user_id
    # if login_user_id != landlord_user_id:
    if order.house.user_id != g.user_id:
        return jsonify(errno=RET.USERERR,errmsg=u'权限不够')
    # 3.修改订单的status属性为'已接单'
    order.status ='WAIT_COMMENT'
    # 4.更新数据到数据库
    try:
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR,errmsg=u'更新订单状态失败')

    # 5.响应结果
    return jsonify(errno=RET.OK,errmsg=u'OK')


@api.route('/orders')
@login_required
def get_order_list():
    """
    获取订单列表
    0.判断用户是否登录,
    1.获取参数,user_id = g.user_id,role判断用户角色是房客还是房东
    2.查询用户user_id对应的订单
    3.构造响应数据
    4.响应结果
    :return:
    """
    # 1.获取参数,user_id = g.user_id
    user_id = g.user_id
    role = request.args.get('role')
    if role not in ['custom','landlord']:
        return jsonify(errno=RET.PARAMERR,errmsg=u'缺少必传参数')

    # 2.查询用户user_id对应的订单
    try:
        # role判断用户角色是房客还是房东
        if role == 'custom':
            orders = Order.query.filter(Order.user_id==user_id).all()
        else:
            # 查询该用户的发布的房屋信息
            houses = House.query.filter(House.user_id ==user_id).all()
            # 获取发布的房屋的ids
            house_ids = [house.id for house in houses]
            # 从订单中查询出house_ids在订单中的id(即查找订单中有没有包含house_ids列表中的house_id的订单)
            orders = Order.query.filter(Order.house_id.in_(house_ids)).all()

    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DATAERR,errmsg=u'查询订单信息失败')
    if not orders:
        return jsonify(errno=RET.NODATA,errmsg=u'订单不存在')
    # 3.构造响应数据
    orders_dict_list = []
    for order in orders:
        orders_dict_list.append(order.to_dict())

    # 4.响应结果
    return jsonify(errno=RET.OK,errmsg=u'OK',data = orders_dict_list)



@api.route('/orders',methods=['POST'])
@login_required
def create_order():
    """创建订单
    0.判断用户是否登录  @login_required
    1.接收参数,house_id,start_date,end_date
    2.校验参数
    3.查询房屋是否被预定
    4.新建order订单模型对象保存订单数据
    5.保存订单数据到数据库
    6.响应结果
    """
    # 1.接收参数,house_id,start_date,end_date
    json_dict = request.json
    house_id = json_dict.get('house_id')
    start_date_str = json_dict.get('start_date')
    end_date_str = json_dict.get('end_date')
    print json_dict
    # 2.校验参数
    # 校验参数完整性
    if not all([house_id,start_date_str,end_date_str]):
        return jsonify(errno=RET.PARAMERR,errmsg=u'缺少参数')
    # 校验入住时间是否小于离开时间
    try:
        start_date = datetime.datetime.strptime(start_date_str,'%Y-%m-%d')
        end_date = datetime.datetime.strptime(end_date_str, '%Y-%m-%d')
        # if not end_date > start_date:
        #     return jsonify(errno=RET.PARAMERR,errmsg=u'入住时间有误')
        if end_date and start_date:
            assert end_date>start_date,Exception(u'入住时间有误')
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR,errmsg=u'入住时间有误')
    #　查询数据库，看house_id对应的房屋是否存在
    try:
        house = House.query.get(house_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg=u'查询房屋信息失败')
    if not house:
        return jsonify(errno=RET.NODATA,errmsg=u'房屋不存在')
    # 查询房屋是否被预定
    try:
        conflict_orders = Order.query.filter(start_date<Order.end_date,end_date>Order.begin_date).all()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg=u'查询冲突时间订单失败')
    # 如果冲突订单有值,说明该房屋已经被预定
    if conflict_orders:
        return jsonify(errno=RET.DATAERR,errmsg=u'房屋已经被预定')
    #3.新建order订单模型对象保存订单数据
    days = (end_date-start_date).days
    order = Order()
    order.user_id = g.user_id
    order.house_id = house_id
    order.begin_date = start_date
    order.end_date = end_date
    order.days = days
    order.house_price = house.price
    order.amount = house.price*days

    #4.保存数据到数据库
    try:
        db.session.add(order)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR,errmsg=u'保存订单信息到数据库失败')

    # 5.响应结果
    return jsonify(errno=RET.OK,errmsg=u'OK')
