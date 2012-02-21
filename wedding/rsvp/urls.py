from django.conf.urls.defaults import patterns, include, url


urlpatterns = patterns('wedding.rsvp.views',
    url('', 'index', name='rsvp'),
)