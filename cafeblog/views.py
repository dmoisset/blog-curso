from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, DetailView
from django.http import HttpResponseRedirect
from cafeblog.forms import NewBlogForm
from cafeblog.models import Blog
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.views.generic import FormView, TemplateView

from cafeblog.forms import SignUpForm


class Index(TemplateView):
    template_name = 'cafeblog/index.html'
index = Index.as_view()


class NewBlog(CreateView):
    pk_url_kwarg = 'blog_pk'
    model = Blog
    form_class = NewBlogForm

    def get_form(self, form_class):
        return super(NewBlog, self).get_form(form_class)

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
        return redirect('cafeblog:index')
signup = SignUp.as_view()
