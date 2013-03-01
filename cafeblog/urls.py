from django.conf.urls import patterns, url

from cafeblog import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),

    url(r'^profile/$', views.profile, name='profile'),
    url(r'^profile_create_edit/$', views.profile_create_edit, name='profile_create_edit'),

    url(r'signup/$', views.signup, name='signup'),
    url(r'blogs_list/$', views.blogs_list, name='blogs_list'),

    #Logueo y Deslogueo
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'cafeblog/login.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/cafeblog'}, name='logout'),

    url(r'^user/password_reset/$',
            'django.contrib.auth.views.password_reset',
            {'post_reset_redirect': '/user/password_reset/done/'},
            name="password_reset",
        ),
    url(r'^user/password_reset/done/$',
            'django.contrib.auth.views.password_reset_done',
        ),

    url(r'^user/password_reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
            'django.contrib.auth.views.password_reset_confirm',
            {'post_reset_redirect': '/user/password_reset/complete/'},
            name='password_reset_confirm',
        ),

    url(r'^user/password_reset/complete/$',
        'django.contrib.auth.views.password_reset_complete',),

    # Blogs management
    url(r'^new_blog/$', views.new_blog, name='new_blog'),
    url(r'^new_blog/$', views.new_blog, name='new_blog'),
    url(r'^(?P<blog_pk>\d+)/$', views.detail, name='detail'),

)
