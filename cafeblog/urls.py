from django.conf.urls import patterns, url
from cafeblog import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),

    #Logueo y Deslogueo
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'cafeblog/login.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
)
