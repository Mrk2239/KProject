from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse, reverse_lazy
from django.views.generic import UpdateView

from users.forms import RegisterForm
from users.models import User

class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            # 不希望用户存在两个，get只能有一个。两个是get失败的一种原因 Q为使用并集查询
            user = User.objects.get(
                Q(username=username) | Q(email=username))
            # django的后台中密码加密：所以不能password==password
            # UserProfile继承的AbstractUser中有def check_password(self,
            # raw_password):
            if user.check_password(password):
                return user
        except Exception as e:
            return None



def register(request):
    #获取跳转地址
    redirect_to = request.POST.get('next',request.GET.get('next',''))
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST,request.FILES)

        if form.is_valid():
            user = form.save()
            messages.success(request, '注册成功，请登录!')

            if redirect_to:
                # 注册后直接登录
                login(request,user)
                return redirect(redirect_to)
            else:
                return redirect(reverse('login'))



    return render(request,'users/register.html',{'form':form,'next':redirect_to})

class UserUpdateView(UpdateView):
    model = User
    fields = ['nickname','email','headshot','signature']
    success_url = reverse_lazy('blog:index')
