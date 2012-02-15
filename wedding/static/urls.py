from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('wedding.static.views',
    url(r'', 'home'),
    url(r'info/', 'info'),
)