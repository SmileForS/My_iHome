# -*- coding:utf-8 -*-
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from iHome_LL import get_app
from iHome_LL import db
from iHome_LL import models

# 创建app
app = get_app('default')
# 创建脚本管理器
manager = Manager(app)

# 让app和db在迁移时建立关联(迁移还没完成，所以没有放进__init__中)
Migrate(app,db)
# 将数据库迁移脚本添加到脚本管理器,'db'是脚本的别名
manager.add_command('db',MigrateCommand)
#



if __name__ == '__main__':
    # app.run(debug=True,host='192.168.241.154')
    print app.url_map
    manager.run()