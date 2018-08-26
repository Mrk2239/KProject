from flask import current_app
from flask_login import UserMixin

from app import db
from itsdangerous import TimedJSONWebSignatureSerializer as JWS

from app.extentions import lm


class User(UserMixin,db.Model):

    # 自定义表名
    __tablename__='user'

    # 定义字段：id,用户名,密码，邮箱，头像
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    username = db.Column(db.String(20),nullable=False,unique=True)
    password = db.Column(db.String(200),nullable=False)
    email = db.Column(db.String(100),nullable=False,unique=True)
    icon = db.Column(db.String(32),default='monkey.jpg')

    # 用户是否激活
    confirmed = db.Column(db.Boolean,default=False)

    # 定义一对多表关系（一个用户发表多篇博文）
    # user1.posts正向引用，动态加载（得到的是BaseQuery），post.user反向引用，懒加载
    posts = db.relationship('Post',lazy='dynamic',backref=db.backref('user',lazy='select'))

    # user.collections查看用户收藏的博文（更高频），正向引用，动态加载（得到的是BaseQuery），post.users，反向引用，动态加载
    collections = db.relationship('Post',lazy='dynamic',secondary='collection',backref=db.backref('users',lazy='dynamic'))

    # 生成用户令牌（token）
    def generate_token(self):
        # 创建TimedJsonWebSignareSerializer对象
        jws = JWS(current_app.config['SECRET_KEY'],expires_in=3600)
        # 压入用户身份信息,生成令牌：jws.dumps:msg->token
        token = jws.dumps({'id':self.id})
        # 返回令牌
        return token.decode()

    # 判断用户是否收藏了某篇博文
    def is_collected(self,pid):

        # 遍历自己的收藏
        for p in self.collections:
            print("is_collected:",pid,p.id)
            if p.id == pid:
                return True

        return False

    @staticmethod
    def check_token(token):

        # 拿到TimedJsonWebSignareSerializer对象
        jws = JWS(current_app.config['SECRET_KEY'])

        # 尝试从jws加载数据
        try:
            # jws.loads: token->msg
            data = jws.loads(token)
        except Exception:
            # 如果发生BadSignature就意味着token是无效的，激活失败
            return False

        # 拿到token中携带的用户信息，将对应的用户激活
        uid =  data.get('id')
        print('check_token,uid=',uid)
        user = User.query.get(uid)
        if user:
            # 激活该用户
            user.confirmed = True
            db.session.add(user)
            return True
        else:
            return False

@lm.user_loader
def get_user(uid):
    return User.query.get(uid)