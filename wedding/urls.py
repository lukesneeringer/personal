from django.conf.urls.defaults import patterns, include, url
from django.conf import settings


urlpatterns = patterns('',
    url(r'^rsvp/', include('wedding.reservations.urls')),
    url(r'^accounts/', include('wedding.accounts.urls')),
    
    # static pages (bundled together in the "static" app)
    url(r'^', include('wedding.static.urls')),
)