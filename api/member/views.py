import logging

from django.db import transaction
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate

from rest_framework import (
    viewsets,
    permissions,
    status,
    mixins
)

from rest_framework.response import Response

from .serializers import (
    UserCreateSerializer,
    JSONWebTokenSerializerWithEmail,
    SocialAuthSerializer,
    UserSerializer,
)

from api.permissions import (
    IsAuthenticatedOrCreationOrReadOnly,
    IsSelf
)

from api.utils import format_response


logger = logging.getLogger('django')

class UserViewSet(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  viewsets.GenericViewSet):

    """
    """

    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticatedOrCreationOrReadOnly, IsSelf, )

    def get_serializer_class(self):
        """we use rest framework url api versioning
        """
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action == 'login':
            return JSONWebTokenSerializerWithEmail
        elif self.action == 'social_login':
            return SocialAuthSerializer

        return super().get_serializer_class()

    def login(self, request, *args, **kwargs):
        """login with email and password

        --swagger schema--

        params:
         - name: email
           required: true
           type: string

         - name: password
           required: true
           type: string

        """
        import pdb; pdb.set_trace()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            obj = serializer.object
            serializer = UserSerializer(obj['user'], context={'request': request})
            data = serializer.data
            data.update({'jwt_token': obj['token']})

            return Response(format_response(200, data=data), status=status.HTTP_200_OK)
        else:
            return Response(format_response(1000, errors=serializer.errors), status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            instance = self.perform_create(serializer)
            headers = self.get_success_headers(serializer.initial_data)

            data = UserSerializer(instance, context={'request': request}).data
            # NOTE: maybe, we need to get jwt_token

            return Response(format_response(200, data=data), status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        return serializer.save()

    def partial_update(self, request, *args, **kwargs):
        return Response(format_response(200, data={}), status=status.HTTP_200_OK)

    def social_login(self, request, *args, **kwargs):
        is_create = True
        data = request.data
        data.update({'service': self.kwargs['service']})
        serializer = self.get_serializer(data=data)

        try:
            serializer.is_valid(raise_exception=True)
            instance = self.perform_create(serializer)
            user = instance['user']
        except serializers.ValidationError as e:
            # note: need to check code params
            if e.code == 1002:
                is_create = False
                instance = serializer._social_data
                user = authenticate(**{'service': self.kwargs['service'].lower(),
                                        'username': serializer._social_data['id']})
                instance.update({'user': user})
            else:
                raise e

        if not user.is_active:
            raise serializers.ValidationError('User account is disabled.', 1000)

        serializer = UserSerializer(user, context={'request': request})
        data = serializer.data

        return Response(format_response(200, data={}), status=status.HTTP_200_OK)
