from django.contrib.auth.decorators import login_required
from django.views.generic import FormView, ListView, TemplateView, CreateView, DetailView
from django.http import HttpResponseRedirect
from cafeblog.forms import NewBlogForm
from cafeblog.models import Blog
from django.contrib.auth.models import User
from django.shortcuts import redirect, render_to_response
from django.contrib import messages
from forms import ProfileForm
from django.core.exceptions import ObjectDoesNotExist
from django.template import RequestContext
from models import UserProfile


from cafeblog.forms import SignUpForm


class Index(TemplateView):
    template_name = 'cafeblog/index.html'
index = Index.as_view()


@login_required
def profile(request):
    try:
        user_profile = request.user.get_profile()
        return render_to_response('cafeblog/profile.html',
                                  {'user_profile': user_profile, },
                                  context_instance=RequestContext(request),)
    except ObjectDoesNotExist:
        redirect('cafeblog:profile_edit')

@login_required
def profile_edit(request):
    try:
        user_profile = request.user.get_profile()
    except ObjectDoesNotExist:
        user_profile = UserProfile(user=request.user)
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=user_profile, label_suffix='')
        if profile_form.is_valid():
            profile_form.save()
            return redirect('cafeblog:profile')
    elif request.method == 'GET':
        profile_form = ProfileForm(instance=user_profile, label_suffix='')
    return render_to_response('cafeblog/profile_edit.html',
                  {'profile_form': profile_form, },
                  context_instance=RequestContext(request))

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
