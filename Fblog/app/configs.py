import os

# app.config.from(Config)
# 写法：属性1=值1，属性2=值2,...
class Config:
    # 全局秘钥
    SECRET_KEY = '123456'

    # 数据库URI
    DATABASE_URI = 'sqlite:////root/venvs/Day8MyBlog/db/blog.sqlite'

    # 数据库配置：URI + 自动提交 + 数据变化免警告
    SQLALCHEMY_DATABASE_URI = DATABASE_URI
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 上传文件允许的最大字节数
    MAX_CONTENT_LENGTH = 8 * 1024 * 1024

    # 配置上传的绝对路径
    UPLOADED_PHOTOS_DEST = os.path.join(os.path.abspath(os.path.dirname(__file__)),'static','uploads')

    # 邮箱配置：邮箱服务器 + 账号信息
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.1000phone.com')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', 'ouyangsuo@1000phone.com')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', '123456')


# 为app配置各种app.config['XXX']
def init_configs(app):
    # 从一个【配置类】中读取各种配置
    app.config.from_object(Config)

# 回归测试，外界导入时不会被导入
if __name__ == '__main__':
    print(os.path.abspath(os.path.dirname(__file__)))