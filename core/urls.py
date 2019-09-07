from django.conf.urls import (include, url)

from django.contrib import admin
from django.conf import settings

from rest_framework.documentation import include_docs_urls
from core import views

urlpatterns = [
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth', include('rest_framework.urls',
                              namespace='rest_framework')),
    url(r'^api/', include('api.urls', namespace='api')),
    url(r'^health/', views.health)
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
