from flask_migrate import MigrateCommand
from flask_script import Manager

# 将app的配置功能封装在app模块下的create_app函数中
from app import create_app

# 将所有的扩展对象封装在app.extentions模块中，其中自然包括SQLAlchemy对象db
from app.extentions import db

'''
manage.py的职能：总调度
所以只应该写调度代码，不应该写具体的业务逻辑代码
'''

# 封装app的初始化过程：创建Flask对象，配置app.config['xxx']，注册蓝图，绑定各种扩展...
app = create_app()

# 配置命令行启动
manager = Manager(app)

# 配置数据迁移命令
manager.add_command('db', MigrateCommand)

# 生成数据库：python manage.py createdb
@manager.command
def createdb():
    db.create_all()

# 运行
if __name__ == '__main__':
    manager.run()
