# -*- coding:utf-8 -*-
# 个人中心
from flask import session,current_app,jsonify,g,request
from iHome_LL import db,constants
from iHome_LL.models import User
from . import api
from iHome_LL.utils.image_storage import upload_image
from iHome_LL.utils.response_code import RET
from iHome_LL.utils.common import login_required


@api.route('/users/auth',methods=['GET'])
@login_required
def get_user_auth():
    """查询实名认证信息"""
    user_id = g.user_id
    # 查询登录的用户的信息
    try:
        user = User.query.get(user_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg=u'查询用户信息失败')
    if not user:
        return jsonify(errno=RET.NODATA,errmsg=u'用户不存在')
    # #获取real_name和id_card
    # real_name = user.real_name
    # id_card = user.id_card
    # 组织响应数据
    response_data = user.auth_to_dict()
    # 响应结果
    return jsonify(errno=RET.OK,errmsg=u'查询实名认证信息成功',data = response_data)

@api.route('/users/auth',methods=['POST'])
@login_required
def set_user_auth():
    """提供用户实名认证
    0.判断用户是否是登录用户, @login_required
    1.接收参数:real_name,id_card
    2.判断参数是否缺少:这里就不对身份证进行格式的校验，省略掉
    3.查询当前的登录用户模型对象
    4.将real_name,id_card赋值给当前用户模型对象
    5.将新的数据写入到数据库
    6.响应结果
    """
    #1.接收参数:real_name,id_card
    json_dict = request.json
    real_name = json_dict.get('real_name')
    id_card = json_dict.get('id_card')

    # 2.判断参数是否缺少:这里就不对身份证进行格式的校验，省略掉
    if not all([real_name,id_card]):
        return jsonify(errno=RET.PARAMERR,errmsg=u'参数有误')
    # 3.查询当前的登录用户模型对象
    user_id =g.user_id
    try:
        user = User.query.get(user_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg=u'查询用户信息失败')
    if not user:
        return jsonify(errno=RET.NODATA,errmsg=u'用户不存在')
    # 4.将real_name,id_card赋值给当前用户模型对象
    user.real_name = real_name
    user.id_card = id_card

    # 5.将新的数据写入到数据库
    try:
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR,errmsg=u'保存实名认证数据失败')

    # 6.响应结果
    return jsonify(errno=RET.OK,errmsg=u'实名认证成功')


@api.route('/users/name',methods=['PUT'])
@login_required
def set_user_name():
    """修改用户名
    0.TODO判断用户是否登陆 @login_required
    1.接收用户传入的新名字 new_name
    2.判断参数是否为空
    3.查询当前登陆用户
    4.将new_name赋值给当前用户的name属性
    5.将新的数据写入数据库
    6.响应结果
    """
    # 1.接收用户传入的新名字 new_name
    json_dict = request.json
    new_name = json_dict.get('name')
    # 2.判断参数是否为空
    if not new_name:
        return jsonify(errno=RET.PARAMERR,errmsg=u'参数错误')
    # 3.查询当前登陆用户
    # user_id = session.get('user_id')
    user_id = g.user_id
    try:
        user = User.query.get(user_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg=u'查询用户信息失败')
    if not user:
        return jsonify(errno=RET.NODATA,errmsg=u'用户不存在')
    # 4.将new_name赋值给当前用户的name属性
    user.name = new_name
    # 5.将新的数据写入数据库
    try:
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR,errmsg=u'修改用户名信息保存失败')
    # 修改用户名时,还需要修改session里面的name
    session['name']=new_name
    #6.响应结果
    return jsonify(errno=RET.OK,errmsg=u'修改用户名成功')

@api.route('/users/avatar',methods=["POST"])
@login_required
def upload_avatar():
    """提供用户头像上传
    0.TODO 先判断用户是否登录
    1.接收请求参数:avatar对应的图片数据,并校验
    2.调用上传图片工具方法
    3.存储图片的key到user.avatar_url属性中
    4.响应上传结果,在结果中传入avatar_url,方便用户上传图像后立刻刷新头像
    """
    # 1.接收请求参数:avatar对应的图片数据,并校验
    try:
        # 这是通过前端ajax模拟form表单传过来的数据，直接用submit按钮提交时，会自动将表单中的name和value提交过来
        image_data = request.files.get('avatar')
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR,errmsg=u'头像参数错误')

    # 2.调用上传图片工具方法
    try:
        key = upload_image(image_data)
        # print key
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.THIRDERR,errmsg=u'头像上传失败')

    # 3.存储图片的key到user.avatar_url属性中
    # 获取登陆用户的user_id
    # user_id = session.get('user_id')
    user_id = g.user_id
    # 查询登陆用户对象
    try:
        user = User.query.get(user_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg=u'查询用户失败')
    if not user:
        return jsonify(errno=RET.NODATA,errmsg=u'用户不存在')

    # 给登陆用户模型属性赋新值
    user.avatar_url = key
    # 将新值保存到数据库
    try:
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR,errmsg=u'存储用户头像地址失败')
    #4.响应上传结果,在结果中传入avatar_url,方便用户上传图像后立刻刷新头像
    #　拼接访问头像的全路径
    # http://oyucyko3w.bkt.clouddn.com/FobMwS7gPtQ6IqTyw_Kt5DfdbKsY
    # avatar_url = "http://oyucyko3w.bkt.clouddn.com/" +key
    # 上面直接将地址放在源代码中的操作有危险，容易被人修改
    avatar_url = constants.QINIU_DOMIN_PREFIX +key
    return jsonify(errno=RET.OK,errmsg=u'上传头像成功',data = avatar_url)




@api.route('/users')
@login_required
def get_user_info():
    """获取用户基本信息
    0.TODO判断用户是否登录
    1.获取登录用户的id
    2.查询出登录用户的基本信息
    3.构造响应数据
    4.响应登录用户信息
    """
    # 1.获取登录用户的id
    # session中没有数据的时候user_id=None
    # user_id = session.get('user_id')
    user_id = g.user_id
    # 2.查询出登录用户的基本信息
    try:
        user = User.query.get(user_id)
        # current_app.logger.debug(user)
    except Exception as e:
        current_app.logger.error(e)
        # 当用户没登录的时候会报这个错误
        return jsonify(errno=RET.DBERR,errmsg=u'查询用户信息失败,请重新登录')
    if not user:
        return jsonify(errno=RET.NODATA,errmsg=u'用户不存在')

    # 3.构造响应数据
    # response_data = {
    #     'avatar_url':user.avatar_url,
    #     'name':user.name,
    #     'mobile':user.mobile,
    #     'user_id':user.id
    # }
    response_data = user.to_dict()
    # 4.响应数据
    return jsonify(errno=RET.OK,errmsg=u'OK',data = response_data)



