from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, DetailView

from cafeblog.models import Blog


class Index(ListView):
    model = Blog
    template_name = 'cafeblog/index.html'
index = Index.as_view()


class NewBlog(CreateView):
    #context_object_name = 'blog'
    pk_url_kwarg = 'blog_pk'
    model = Blog
new_blog = NewBlog.as_view()


class BlogDetails(DetailView):
    context_object_name = 'blog'
    pk_url_kwarg = 'blog_pk'
    model = Blog
detail = BlogDetails.as_view()