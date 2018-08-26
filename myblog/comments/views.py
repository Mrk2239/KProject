from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.urls import reverse
from django.views.generic import CreateView

from blog.models import Post
from comments.forms import CommentForm
from comments.models import Comment


def post_comment(request,pk):
    post = get_object_or_404(Post,pk=pk)
    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            #comment.post = post
            comment.post_id = pk
            comment.save()
        #数据有误,需保存form表单所写的数据
        else:

            comment_list = post.comment_set.all()
            context = {
                'post':post,
                'form':form,
                'comment_list':comment_list,
            }

            return render(request,'blog/detail.html',context=context)

    #return redirect(reverse('blog:post_detail',kwargs={'pk':pk}))
    return redirect(post)

#改用通用视图类
class CommentCreateView(CreateView):
    model = Comment
    fields = ['name', 'email', 'url', 'text']
    template_name = 'blog/detail.html'
    context_object_name = 'comment_list'

    #重写get_success_url方法,重定向
    def get_success_url(self):
        return reverse('blog:post_detail',kwargs={'pk':self.kwargs['pk']})

    #重写form_vaild方法,补全comment需要的post,返回一个httpresponse
    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)

    #重写get_context_data方法
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        #往context中添加我们自己的上下文
        post = get_object_or_404(Post,pk=self.kwargs['pk'])
        context.update({
            'post':post,
            'comment_list':post.comment_set.all()
        })

        return context

    #当form表单校验失败时,执行form_invalid方法
    def form_invalid(self, form):
        #return super().form_invalid(form)
        post = get_object_or_404(Post,pk = self.kwargs['pk'])
        return render(self.request,'blog/detail.html',{
            'post':post,
            'comment_list':post.comment_set.all()
        })

