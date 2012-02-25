from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from django.contrib.auth import views


urlpatterns = patterns('',
    # authentication management
    url(r'^%s$' % settings.LOGIN_URL[1:], views.login, name='login'),
    url(r'^%s$' % settings.LOGOUT_URL[1:], views.logout_then_login, name='logout'),
    url(r'^accounts/password-change/$', views.password_change, name='password-change'),
    url(r'^accounts/password-change-done/$', views.password_change_done),

    # rsvp app
    url(r'^rsvp/', include('wedding.reservations.urls')),
    
    # static pages (bundled together in the "static" app)
    url(r'^', include('wedding.static.urls')),
)