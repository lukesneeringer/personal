from django.conf.urls.defaults import patterns, include, url


urlpatterns = patterns('wedding.reservations.views',
    url('', 'index', name='rsvp'),
)