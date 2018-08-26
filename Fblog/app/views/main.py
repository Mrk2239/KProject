from flask import Blueprint,render_template,redirect,url_for,flash,request
from app.extentions import db
from app.forms import PostForm
from app.models import User,Post
from flask_login import login_required,current_user

'''
封装了所有与主页相关的视图函数
'''

# 定义蓝图
mainbp = Blueprint('mainbp', __name__)

# /?page=3
# 首页路由函数
@mainbp.route('/',methods=['GET','POST'])
def index():

    # 创建博文编辑表单
    form = PostForm()

    # 预校验博客正文
    if form.validate_on_submit():

        # 拿到用户编辑的博文
        content = form.content.data

        # 拿到当前用户（博主）
        user = current_user._get_current_object()
        # 插入博文对象，同时关联其博主
        post = Post(content=content,user=user)
        db.session.add(post)

        '''
        方式二：
        user = current_user._get_current_object()
        post = Post(content=content,user=user)
        user.posts.append(post)
        db.session.add(user)
        '''

        # 推送flash消息
        flash('发表成功！')

    # 展示所有内容
    # 拿到GET请求参数
    page = int(request.args.get('page',1))

    # 获取分页器，内容按发布时间降序，每页5条，当前给出第3页数据，页码错误时不抛404而是返回第1页
    pagination = Post.query.order_by(Post.posttime.desc()).paginate(page=page, per_page=5, error_out=False)

    # 获得第3页的博文数据
    posts = pagination.items

    # 将编辑表单丢给页面渲染
    return render_template('main/index.html',form=form,posts=posts,pagination=pagination,page=page)

@mainbp.route('/getmoney/')
@login_required
def getmoney():
    return '您可以免费在这里学习Python并到前台领取劳斯莱斯一辆'