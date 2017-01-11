from django.conf.urls import url, include

from rest_framework import permissions

from .views import UserViewSet


urlpatterns = [
    url(r'^$', UserViewSet.as_view({'get': 'list'}), name='user_list'),
    url(r'^(?P<pk>[0-9]+)/$', UserViewSet.as_view({'patch': 'partial_update'}), name='detail_update'),
    url(r'^login/$', UserViewSet.as_view(
        {'post': 'login'},
        permission_classes=(permissions.AllowAny, )),
        name='login'),

    url(r'^login/(?P<service>\w+)/$', UserViewSet.as_view(
        {'post': 'social_login'},
        permission_classes=(permissions.AllowAny, )),
        name='social_login'),
]
