from django.conf import settings
from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.contrib.sites.models import Site

# get the current site
site = Site.objects.get_current()

# enable the admin
admin.autodiscover()

urlpatterns = patterns('',
    # django admin
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

# add URLs based on what site I'm on...
# if site.domain == 'luke-and-meagan.com':
if settings.SITE_ID == 1:
    urlpatterns += patterns('', url(r'', include('wedding.urls')))