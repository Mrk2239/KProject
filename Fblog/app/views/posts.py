from flask import Blueprint,flash,redirect,url_for, jsonify
from flask_login import login_required,current_user
from wtforms.ext import sqlalchemy

from app import db
from app.models import Post


'''
封装了所有与博文相关的视图函数
'''

# 定义蓝图
postbp = Blueprint('postbp', __name__)

@postbp.route('/showall/')
def showall():
    return 'showall'\

@postbp.route('/post/')
@login_required
def post():
    flash('发布成功！')
    return redirect(url_for('mainbp.index'))

# 切换博文的收藏状态
@postbp.route('/switch_collect/<int:pid>/')
@login_required
def switch_collect(pid):
    # 根据id找出博文
    post = Post.query.get(pid)

    # 切换收藏状态
    if current_user.is_collected(pid):

        # 如果已收藏就remove掉
        current_user.collections.remove(post)
        # 已经配置了自动提交
        # db.session.add(current_user)

        # 给前端返回json
        return jsonify({'result':False})
    else:
        # 如果未收藏就添加到收藏中
        current_user.collections.append(post)
        # 已经配置了自动提交
        # db.session.add(current_user)

        # 给前端返回json
        return jsonify({'result': True})



