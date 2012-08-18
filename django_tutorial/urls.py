from django.conf import settings
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
if settings.DEBUG:
    from django.contrib import admin
    admin.autodiscover()

urlpatterns = patterns('',
    url(r'', include('frontend.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^admin/', include(admin.site.urls)),
    )