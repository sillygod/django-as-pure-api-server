from django.conf.urls import (
    include,
    url
)

from django.contrib import admin


urlpatterns = [
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/', include('api.urls', namespace='api'))
]
