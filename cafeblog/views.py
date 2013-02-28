from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import FormView, TemplateView, ListView

from cafeblog.forms import SignUpForm
from cafeblog.models import Blog


class Index(TemplateView):
    template_name = 'cafeblog/index.html'
index = Index.as_view()


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


class BlogList(ListView):
    def get_queryset(self, **kwargs):
        return Blog.objects.filter(authors=self.request.user)
    context_object_name = 'blogs_list'
    template_name = 'cafeblog/blogs_list.html'
blogs_list = login_required(BlogList.as_view())
