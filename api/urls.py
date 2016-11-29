from django.conf.urls import (
    url,
    include
)


urlpatterns = [
    url(r'^(?P<version>(v1|v2))/member/', include('api.member.urls', namespace='member')),
]
