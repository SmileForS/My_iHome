# -*- coding:utf-8 -*-
import redis
class Config(object):
    """加载配置"""
    # 开启调试模式
    DEBUG = True

    # 秘钥
    SECRET_KEY = '8hV4rv0opNaPoWc/lbCTsLc70IXTgRD3R+AtQMyvtwzuoFGk0TiWEg7cPwNoV1mp'
    # 配置mysql数据库:开发中使用真实IP
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@127.0.0.1:3306/iHome'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 配置redis
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379

    # 配置session数据存储到redis数据库
    SESSION_TYPE = 'redis'
    # 指定存储session数据的redis的位置
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST,port=REDIS_PORT)
    # 开启session数据的签名,意思是让session数据不以明文形式存储
    SESSION_USE_SIGNER = True
    # 设置session的会话的超时时长
    PERMANENT_SESSION_LIFETIME = 3600*24