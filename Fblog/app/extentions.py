from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_moment import Moment
from flask_uploads import UploadSet,IMAGES, configure_uploads
from flask_sqlalchemy import SQLAlchemy

# 各种扩展对象
db = SQLAlchemy()
migrate = Migrate(db=db)
bs = Bootstrap()

# 发邮件扩展
mail = Mail()

# 配置LoginManager的配置
lm = LoginManager()
lm.login_view = 'userbp.login'
lm.login_message = 'login required!'
lm.session_protection = 'strong'

# 上传扩展扩展对象，允许的格式为图片
photos = UploadSet('photos', IMAGES)

moment = Moment()

# 为各种扩展绑定app
# 使用的是事后绑定——因为app诞生的很晚，但各种扩展被依赖的很早
def init_extentions(app):

    # 为扩展对象绑定app
    db.init_app(app)
    migrate.init_app(app)
    bs.init_app(app)

    # 为mail绑定app
    mail.init_app(app)
    moment.init_app(app)
    lm.init_app(app)

    # 绑定app和US对象photos
    configure_uploads(app, photos)