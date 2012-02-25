from django.conf.urls.defaults import patterns, include, url


urlpatterns = patterns('wedding.reservations.views',
    url(r'^$', 'index', name='rsvp'),
    url(r'^set/$', 'rsvp_form', name='rsvp-form'),
    url(r'^thank-you/$', 'rsvp_thanks', name='rsvp-thanks'),
)