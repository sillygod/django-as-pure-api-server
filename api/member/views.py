from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

from rest_framework import (
    viewsets,
    permissions,
    status,
    mixins
)

from .serializers import (
    UserSerializer,
    UserSerializerNew
)


class UserViewSet(mixins.ListModelMixin,
                  viewsets.GenericViewSet):

    """
    """

    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

    def get_serializer_class(self):
        if self.request.version == 'v1':
            return UserSerializer
        elif self.request.version == 'v2':
            return UserSerializerNew

        return super().get_serializer_class()


