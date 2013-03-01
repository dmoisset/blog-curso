from django.contrib.auth.decorators import login_required
from django.views.generic import FormView, ListView, TemplateView, CreateView, DetailView, ArchiveIndexView
from django.http import HttpResponseRedirect
from cafeblog.forms import NewBlogForm
from cafeblog.models import Blog
from django.contrib.auth.models import User
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages

from cafeblog.forms import SignUpForm


ARTICLE_PAGINATE_BY = 5


class Index(TemplateView):
    template_name = 'cafeblog/index.html'
index = Index.as_view()


class NewBlog(CreateView):
    pk_url_kwarg = 'blog_pk'
    model = Blog
    form_class = NewBlogForm

    def form_valid(self, form):
        user = User.objects.get(pk=self.request.user.pk)
        blog = Blog(
            title=form.cleaned_data['title'],
            description=form.cleaned_data['description'],
            administrator=user
        )
        blog.save()
        self.object = blog
        user.blog_set.add(blog)

        return HttpResponseRedirect(self.get_success_url())

new_blog = login_required(NewBlog.as_view())


class BlogDetails(DetailView):
    context_object_name = 'blog'
    pk_url_kwarg = 'blog_pk'
    model = Blog
detail = BlogDetails.as_view()


class SignUp(FormView):
    form_class = SignUpForm
    template_name = 'cafeblog/signup.html'
    success_url = '/'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()

        messages.add_message(self.request,
            messages.INFO,
            u'Sign Up Success. Please Login and enjoy the CafeBlog.'
        )
        return redirect('cafeblog:login')
signup = SignUp.as_view()


class BlogList(ListView):
    def get_queryset(self, **kwargs):
        return Blog.objects.filter(authors=self.request.user)
    context_object_name = 'blogs_list'
    paginate_by = 10
    template_name = 'cafeblog/blogs_list.html'
blogs_list = login_required(BlogList.as_view())


class PaginatePostList(ArchiveIndexView):
    paginate_by = ARTICLE_PAGINATE_BY
    date_field = 'pub_date'
    template_name = 'cafeblog/blog_archive.html'
    allow_empty = True

    def get_queryset(self):
        b = get_object_or_404(Blog, pk=self.kwargs['blog_pk'])
        return b.post_set.all().order_by('-pub_date')

archive = PaginatePostList.as_view()
