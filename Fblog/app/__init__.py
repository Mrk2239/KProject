from flask import Flask
from flask import render_template

from app.configs import init_configs
from app.extentions import db, init_extentions

# 将所有蓝图对象封装在视图包模块app.views中
from app.views import mainbp,postbp,userbp

'''
封装了整个应用的创建、蓝图注册、错误处理
之所以没有将蓝图和错误处理抽取为单独的模块，一是因为和app的关系紧密，二是因为它们的代码量暂时还很小
'''

# 全局蓝图元组
blueprints = (
    (mainbp,'/blog'),
    (userbp,'/blog/user'),
    (postbp,'/blog/post')
)

# 注册应用的所有蓝图
def config_blueprints(app):
    # 遍历全局蓝图元组，注册所有蓝图
    for name,prefix in blueprints:

        # 注册蓝图，参数：蓝图名称，蓝图前缀
        app.register_blueprint(name, url_prefix=prefix)

# 声明全局错误处理
def config_errorhandlers(app):

    # 为app注册全局的404错误处理器
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('error/404.html')

# 配置全局app对象
def create_app():

    # 创建应用对象
    app = Flask(__name__)

    # 注册蓝图
    config_blueprints(app)

    # 定义错误处理
    config_errorhandlers(app)

    # 全局配置参数，SECRET_KEY...
    init_configs(app)

    # 配置所有扩展
    init_extentions(app)

    # 返回配置好的app
    return app