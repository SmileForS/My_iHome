# -*- coding:utf-8 -*-
# 个人中心
from flask import request
from flask import session,current_app,jsonify
from iHome_LL import db,constants
from iHome_LL.models import User
from . import api
from iHome_LL.utils.image_storage import upload_image
from iHome_LL.utils.response_code import RET

@api.route('/users/avatar',methods=["POST"])
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
    user_id = session.get('user_id')
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
    user_id = session.get('user_id')
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
    response_data = {
        'avatar_url':user.avatar_url,
        'name':user.name,
        'mobile':user.mobile,
        'user_id':user.id
    }
    # 4.响应数据
    return jsonify(errno=RET.OK,errmsg=u'OK',data = response_data)



