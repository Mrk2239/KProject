import threading

from flask import Blueprint, render_template,url_for,current_app,redirect,flash
from flask_login import login_user,current_user,logout_user,login_required
from flask_mail import Message
from app.extentions import mail, db, photos, lm
from app.forms import RegisterForm, LoginForm,UploadForm,ProfileForm
from app.models import User
from app.utils import sendmail

'''
封装了所有与用户管理相关的视图函数
'''

# 定义蓝图
userbp = Blueprint('userbp', __name__)


# 注册视图函数
@userbp.route('/register/', methods=['GET', 'POST'])
def register():
    # 创建包含了字段定义和预校验规则的FlaskForm对象
    form = RegisterForm()

    # 检验用户的提交是否符合预校验规则
    if form.validate_on_submit():

        '''
        通过预校验以后执行真正的注册逻辑
        '''

        # 提取表单数据
        username = form.username.data
        password = form.password.data
        email = form.email.data
        print(username,password,email)

        # 插入新的用户
        user = User(username=username,password=password,email=email)
        db.session.add(user)
        db.session.commit()

        # 构造激活链接，当用户点击激活链接时访问激活路由，校验token
        # 校验通过以后将用户的confirmed设置为True，代表已激活
        # _external=True构建完整url，不写时构建的url不包含host部分
        activate_url = url_for('userbp.activate',token=user.generate_token(),_external=True)
        print("activate_url=",activate_url)

        # 发送激活邮件
        msg = Message(
            subject='please activate your email',
            recipients=[user.email],
            body='click <a href="'+activate_url+'">here</a> to acivate your email',
            html='click <a href="'+activate_url+'">here</a> to acivate your email',
            sender = current_app.config['MAIL_USERNAME']
        )

        # 异步发送邮件
        threading.Thread(target=sendmail,args=(current_app._get_current_object(),msg)).start()

        # 提示注册成功
        return '注册成功！'

    # 第一义访问或预校验失败都返回渲染后的注册页面
    return render_template('user/register.html', form=form)

@userbp.route('/activate/<token>')
def activate(token):
    if User.check_token(token):
        return '激活成功！'
    else:
        return '激活失败！'

# 定义登录视图函数
@userbp.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():

        # 从表单中获取数据
        username = form.username.data
        password = form.password.data
        remember = form.remember.data
        print(username,password,remember)

        # 查询用户是否存在
        u = User.query.filter(User.username==username,User.password==password).first()
        if u:
            # 校验通过，调用flask-login的login_user方法，并配置记住用户名
            login_user(u, remember=remember)

            print('登录成功！',current_user._get_current_object().username)
            return redirect(url_for('mainbp.index'))
        else:
            return '查无此人！'

    return render_template('user/login.html', form=form)

@userbp.route('/logout/')
def logout():
    # 调用flask-login框架的登出方法
    logout_user()
    return redirect(url_for('mainbp.index'))


@userbp.route('/upload_icon/', methods=['GET', 'POST'])
# 必须登录才能访问
@login_required
def upload_icon():
    # 构造上传表单对象
    form = UploadForm()

    # 预校验
    if form.validate_on_submit():
        # 拿到上传的文件
        file = form.file.data

        # 使用US对象保存文件
        filepath = photos.save(file,name=file.filename)
        current_user.icon = file.filename

    # 拿到当前用户头像的访问url
    url = photos.url(   current_user.icon  )

    # 渲染页面
    return render_template('user/upload.html', form=form,imgurl=url)

# 查看用户资料
@userbp.route('/profile/')
def profile():
    form = ProfileForm()

    # flask-login框架的current_user对象就是当前已经登录了的User对象
    form.username.data = current_user.username
    form.email.data = current_user.email

    return render_template('user/profile.html', form=form)
