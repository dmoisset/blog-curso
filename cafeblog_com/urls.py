from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.autodiscover()


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', include('cafeblog.urls', namespace="cafeblog")),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'cafeblog/login.html'}),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'cafeblog/logout.html'}),
)

urlpatterns += staticfiles_urlpatterns()
