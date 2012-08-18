from django.conf.urls import patterns, include, url

from views import *

urlpatterns = patterns('',
    url(r'^$', index, name='index'),
    url(r'^tutorial/start/$', tutorial_start, name='tutorial_start'),
    url(r'^tutorial/(?P<tutorial_id>\d+)/$', tutorial, name='tutorial'),
    url(r'^tutorial/(?P<tutorial_id>\d+)/(?P<step_id>\d+)/$', tutorial_step, name='tutorial_step'),
    url(r'^tutorial/(?P<tutorial_id>\d+)/(?P<step_id>\d+)/run/$', tutorial_step_run, name='tutorial_step_run')
)
