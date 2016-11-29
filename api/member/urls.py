from django.conf.urls import url, include

from .views import UserViewSet


urlpatterns = [
    url(r'^$', UserViewSet.as_view({'get': 'list'}), name='user_list'),
]
