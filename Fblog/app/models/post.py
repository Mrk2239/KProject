from datetime import datetime

from app import db


class Post(db.Model):

    # 表名
    __tablename__='post'

    # ArgumentError:Mapper Mapping|Post|post could not assemble any primary key column for table 'post'

    # id，内容，发布时间
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    content = db.Column(db.Text,nullable=False)
    posttime = db.Column(db.DateTime,default=datetime.utcnow)

    # 用户发表博文（O2M）,多方持有外键
    uid = db.Column(db.Integer,db.ForeignKey('user.id'))