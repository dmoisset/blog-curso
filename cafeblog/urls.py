from django.conf.urls import patterns, url

from cafeblog import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    #Logueo y Deslogueo
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'cafeblog/login.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),

    url(r'^user/password_reset/$', 
            'django.contrib.auth.views.password_reset', 
            {'post_reset_redirect' : '/user/password_reset/done/',
            'template_name':'cafeblog/registration/password_reset_form.html',
            'email_template_name' : 'cafeblog/registration/password_reset_email.html'},
            name="password_reset"
        ),
    url(r'^user/password_reset/done/$',
            'django.contrib.auth.views.password_reset_done',
            {'template_name':'cafeblog/registration/password_reset_done.html'}
        ),

    url(r'^user/password_reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 
            'django.contrib.auth.views.password_reset_confirm', 
            {'post_reset_redirect' : '/user/password_reset/complete/',
            'template_name' : 'cafeblog/registration/password_reset_confirm.html'},
            name='password_reset_confirm'
        ),

    url(r'^user/password_reset/complete/$', 
        'django.contrib.auth.views.password_reset_complete',
        {'template_name' : 'cafeblog/registration/password_reset_complete.html'},)
)
