from django.conf.urls import url
from rest_framework import permissions
from .views import MessageViewSet
from api.permissions import IsSelf

app_name = 'message'

urlpatterns = [
    url(r'^$',
        MessageViewSet.as_view({
            'get': 'list',
            'post': 'post_message'
        }),
        name='message_list'),
    url(r'^(?P<pk>[0-9]+)/$',
        MessageViewSet.as_view({
            'post': 'reply_message',
        }),
        name='reply_message'),
    url(r'^(?P<pk>[0-9]+)$',
        MessageViewSet.as_view({'patch': 'partial_update'},
                               permission_classes=(IsSelf, )),
        name='update_message'),
]
