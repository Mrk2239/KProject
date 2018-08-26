from app.extentions import db

# 导入所有数据模型，方便将来from app.modles import *
from app.models.post import Post
from app.models.user import User

# 用户-博文（M2M）中间表
collection = db.Table(
    # 表名
    'collection',

    # 定义（联合主键）

    # 定义uid列，整型，指向user表的id字段，主键之一
    db.Column('uid',db.Integer, db.ForeignKey('user.id'),primary_key=True),

    # 定义pid列，整型，指向post表的id字段，主键之一
    db.Column('pid',db.Integer, db.ForeignKey('post.id'),primary_key=True)
)

