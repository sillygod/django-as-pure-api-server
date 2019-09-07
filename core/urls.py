from django.conf.urls import (include, url)

from django.contrib import admin
from django.conf import settings

from rest_framework.documentation import include_docs_urls
from django.urls import path

from rest_framework import permissions
from rest_framework.schemas import get_schema_view
from core import views

urlpatterns = [
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth', include('rest_framework.urls',
                              namespace='rest_framework')),
    url(r'^api/', include('api.urls', namespace='api')),
    url(r'^health/', views.health),
    path('openapi',
         get_schema_view(title="Demo Project",
                         description="API docs",
                         permission_classes=(permissions.AllowAny, ),
                         urlconf='api.urls',
                         version="1.0.0"),
         name='openapi-schema'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
