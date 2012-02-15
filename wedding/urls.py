from django.conf.urls.defaults import patterns, include, url


urlpatterns = patterns('',
    url(r'^rsvp/', include('wedding.rsvp.urls')),
    url(r'^', include('wedding.static.urls')),
)