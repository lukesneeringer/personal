from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from django.contrib.auth import views


urlpatterns = patterns('wedding.accounts.views',
    # authentication management
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, { 'next_page': '/' }, name='logout'),
    url(r'^password-change/$', views.password_change, name='password-change'),
    url(r'^password-change-done/$', views.password_change_done),
    url(r'^register/$', 'register', name='register'),
)