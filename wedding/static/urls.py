from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('wedding.static.views',
    url(r'^$', 'home', name='home'),
    url(r'^info/(?P<template_name>[\w\d-]+)/$', 'info', name='info'),
)