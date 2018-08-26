from django.shortcuts import get_object_or_404
from django.template.defaulttags import comment
from django.test import TestCase

# Create your tests here.
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView

from blog.models import Post
from comments.forms import CommentForm


class CommentCreateView(CreateView):
    model = comment
    fields = ['name', 'email', 'url','text','post']
    template_name = 'blog/detail.html'
    # post = get_object_or_404(Post,id=pk)

    def get_success_url(self):
        return reverse('blog:post_detail',kwargs={'pk':self.object.post_id})