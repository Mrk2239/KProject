
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import render, get_object_or_404

# Create your views here.

import markdown

from django.views.generic import ListView, DetailView
from django.views.generic.detail import SingleObjectMixin
from markdown.extensions.toc import TocExtension, slugify

from .utils import custom_paginator
from blog.models import Post, Tag
from comments.forms import CommentForm


def index(request):
    post_list = Post.objects.all()
    #生成一个分页器的实例对象
    paginator  = Paginator(post_list,2)

    page = request.GET.get('page')

    try:
        posts = paginator.page(page)

    except PageNotAnInteger:
        posts = paginator.page(1)

    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request,'blog/index.html',{'posts':posts})




class PostListView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    paginate_by = 2


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 从context中获取我们需要的数据
        paginator = context.get('paginator')
        page_obj = context.get('page_obj')

        # 获取当前页page_obj.number
        start, end = custom_paginator(current_page=page_obj.number, num_pages=paginator.num_pages, max_page=5)
        context.update({
            'page_range': range(start, end+1)
        })
        return context



def post_detail(request,pk):
    post = get_object_or_404(Post,pk=pk)
    post.content = markdown.markdown(post.content,
    extensions=[
    'markdown.extensions.extra',
    'markdown.extensions.codehilite',
    'markdown.extensions.toc', ])

    form = CommentForm()
    comment_list = post.comment_set.all()
    post.increase_views()
    return render(request,'blog/detail.html',locals())

#将post_detail改成通用视图类
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    '''
        def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    '''
    #重写get方法,修改默认行为,调用increase_view方法
    # get方法返回的是一个HttpResponse实例
    def get(self,request,*args,**kwargs):
    #先调用父类的get方法
        response = super().get(request,*args,**kwargs)
        #调用increase_view()方法
        self.object.increase_views()

        return response

    def get_object(self, queryset=None):
        #调用父类的get_object,获取单个对象实例
        self.object =super().get_object(queryset=None)

        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
            TocExtension(slugify=slugify),
        ])

        self.object.content = md.convert(self.object.content)
        self.object.toc = md.toc
        #返回对象
        return self.object

    # 重写get_context_data方法，放入我们自己的上下文
    def get_context_data(self, **kwargs):
        #调用父类的get_context_data方法,以获取当前的context对象
        context = super().get_context_data(**kwargs)
        #分页
        commnet_list = self.object.comment_set.all()
        #对comment_list 进行分页
        paginator = Paginator(commnet_list,2)
        #从request中获取page
        page = self.request.GET.get('page',None)

        try:
            comments = paginator.page(page)
        except PageNotAnInteger:
            #显示第一页,即首页
            comments = paginator.page(1)
        except EmptyPage:
            comments = paginator.page(paginator.num_pages)

        start,end = custom_paginator(current_page=comments.number,num_pages=paginator.num_pages,max_page=5)

        context.update(
            {
                'form': CommentForm(),
                'comments':comments,
                'page_range': range(start,end + 1)
            }
        )
        return context

#优化postdetailview
class PostDetailViewPrime(SingleObjectMixin,ListView):
    paginate_by = 2
    template_name = 'blog/detail.html'

    #重写get方法,调用increase_view方法
    def get(self,request,*args,**kwargs):
        #生成self.object
        self.object = self.get_object()
        #调用increase_view
        self.object.increase_views()
        #最后调用父类的get,返回一个response
        return super().get(request,*args,**kwargs)

    #重写get_object方法,加入markdown渲染的代码
    def get_object(self, qureyset=Post.objects.all()):
        post = super().get_object(queryset=Post.objects.all())
        #进行markdown处理
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            TocExtension(slugify=slugify)
        ])
        post.content = md.convert(post.content)
        #增加目录
        post.toc = md.toc
        #返回对象
        return post

    #重写get_context_data方法,来增加额外的的上下文变量
    def get_context_data(self, **kwargs):
        #先调用父类的get_context_data方法获取context对象
        context = super().get_context_data(**kwargs)
        form = CommentForm
        page_obj = context.get('page_obj',None)
        paginator = context.get('paginator',None)
        start,end = custom_paginator(current_page=page_obj.number,num_pages=paginator.num_pages,max_page=4)
        context.update({
            'post':self.object,
            'form':form,
            'page_range':range(start,end+1)
        })
        return context

    def get_queryset(self):
        return self.object.comment_set.all()

class ArchivesListView(PostListView):

    #重写get_queryset方法,获得post_list返回到 template_name = 'blog/index.html'
    def get_queryset(self):
        return super().get_queryset().filter(created_time__year=self.kwargs['year'],created_time__month=self.kwargs['month'])

#归档
class CategoryListView(PostListView):

    #重写get_queryset方法,获得post_list返回到 template_name = 'blog/index.html'
    def get_queryset(self):
        return super().get_queryset().filter(category_id=self.kwargs['pk'])





class TagListView(PostListView):
    #多对多
    #重写get_queryset方法,获得post_list返回到 template_name = 'blog/index.html'
    # def get_queryset(self):
    #     return super().get_queryset().filter(tag_id=self.kwargs['pk'])
    '''
      def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()
    '''
    #
    # def get_queryset(self):
    #
    #     return super().get_queryset().filter(tags__id=self.kwargs['pk']).order_by('-created_time')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = get_object_or_404(Tag, pk=self.kwargs['pk'])
        #print(tag)
        context.update(
            {'post_list':tag.post_set.all()}
        )
        #print(tag.post_set.all())
        return context

def search(request):
    q = request.GET.get('q')
    print(q)
    msg = ''

    if not q:
        msg = '请重新搜索'
        return render(request,'blog/index.html',{'msg':msg})

    post_list = Post.objects.filter(Q(title__icontains=q)|Q(content__icontains=q)|Q(author__username__icontains=q))

    return render(request,'blog/index.html',{'msg':msg,'post_list':post_list})