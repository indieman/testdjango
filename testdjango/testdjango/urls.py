from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^blog/', include('blog.urls')),
    (r'^comments/', include('django.contrib.comments.urls')),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}),
)

urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG is False:
    urlpatterns += patterns('',
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.STATIC_ROOT}),
    )