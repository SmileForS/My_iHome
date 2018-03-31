# -*- coding:utf-8 -*-
from flask import Flask
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
import redis
from flask_migrate import Migrate,MigrateCommand
# session在flask中的扩展包
from flask_session import Session


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

app = Flask(__name__)

# 加载配置项
app.config.from_object(Config)
#　创建数据库链接对象
db = SQLAlchemy(app)
# 创建redis链接对象
redis_store = redis.StrictRedis(host=Config.REDIS_HOST,port=Config.REDIS_PORT)

# 开启csrf防护
CSRFProtect(app)

# 创建脚本管理器
manager = Manager(app)

# 让app和db在迁移时建立关联
Migrate(app,db)
# 将数据库迁移脚本添加到脚本管理器,'db'是脚本的别名
manager.add_command('db',MigrateCommand)

# 使用session在flask扩展实现将session数据存储在redis
Session(app)


@app.route('/',methods=['GET','POST'])
def index():
    # 测试redis链接
    # redis_store.set('name2','SS')

    # 测试session：flask自带的session模块，用于存储session
    from flask import session
    session['name'] = 'sz_LL'


    return 'index'


if __name__ == '__main__':
    # app.run(debug=True,host='192.168.241.154')
    manager.run()