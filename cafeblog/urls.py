from django.conf.urls import patterns, url

from cafeblog import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^profile_edit/$', views.profile_edit, name='profile_edit'),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'cafeblog/login.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/cafeblog/'}, name='logout'),
)
