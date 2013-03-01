from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.views.generic import FormView, ListView, TemplateView, CreateView, DetailView
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.models import User
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.template.response import TemplateResponse
from django.db import IntegrityError

from cafeblog.forms import NewBlogForm, ArticleForm
from cafeblog.models import Blog, Article
from cafeblog.forms import SignUpForm


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
    template_name = 'cafeblog/blogs_list.html'
blogs_list = login_required(BlogList.as_view())



NO_UNIQUE_TITLE_ERROR = "Such article's title already exist in this blog."
@login_required
def edit_article(request, blog_pk, article_pk=None):
    if blog_pk is None:
        raise Http404(u"No blog specified.")
    blog = get_object_or_404(Blog, pk=blog_pk)

    article = None
    if article_pk:
        article = get_object_or_404(Article, pk=article_pk)
        # TODO: check permissions and authoring
        #if article.created_by != request.user:
        #    raise PermissionDenied

    if request.method == "POST":
        article_form = ArticleForm(request.POST, instance=article)
        if article_form.is_valid():
            author = User.objects.get(pk=request.user.pk)
            now = timezone.now()
            publish = article_form.cleaned_data['is_published']
            pub_date = publish and now or None
            article = Article(
                    blog = blog,
                    title = article_form.cleaned_data['title'],
                    contents = article_form.cleaned_data['contents'],
                    pub_date = pub_date,
                    creation_time = now,
                    last_modified = now,
                    is_published = publish,
                    author = author,
                )
            try:
                article.save()
                blog.article_set.add(article)
                author.article_set.add(article)
                return redirect('cafeblog:article_detail', blog_pk=blog.pk, article_pk=article.pk)
            except IntegrityError, e:
                article_form = ArticleForm(instance=article)
                article_form.errors['title'] = [NO_UNIQUE_TITLE_ERROR]
    else:
        article_form = ArticleForm(instance=article)
    #
    return TemplateResponse(
            request,
            "cafeblog/article_form.html", 
            {'blog_pk':blog.pk, 'blog':blog, "article_form":article_form}
        )



def article_detail(request, blog_pk, article_pk):
    #TODO: check blog_pk and article_pk corresponds
    article = get_object_or_404(Article, pk=article_pk)
    
    # TODO: check permissions and authoring
    #if article.created_by != request.user:
    #    raise PermissionDenied

    if request.method == "GET":
        article_form = ArticleForm(instance=article)
    #
    print "a ver", article_form
    return TemplateResponse(
            request,
            "cafeblog/article_detail.html", 
            {"article":article}
        )
