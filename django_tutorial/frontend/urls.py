from django.conf.urls import patterns, include, url

from views import *

urlpatterns = patterns('',
    url(r'^$', index, name='index'),
    url(r'^tutorial/start/$', tutorial_start, name='tutorial_start'),
    url(r'^tutorial/(?P<tutorial_id>\d+)/$', tutorial, name='tutorial')
)
