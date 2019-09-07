from django.db import transaction
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from rest_framework import serializers

from rest_framework import (viewsets, permissions, status, mixins)

from rest_framework.response import Response

from api.permissions import (IsAuthenticatedOrCreationOrReadOnly, IsSelf)
from api.utils import format_response

from .models import Message

from .serializers import (
    MessageSerializer,
    MessageCreateSerializer,
    MessageReplySerializer,
    MessageUpdateSerializer,
)


class MessageViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                     mixins.UpdateModelMixin, viewsets.GenericViewSet):

    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = (IsAuthenticatedOrCreationOrReadOnly, )

    def get_serializer_class(self):
        serializer_map = {
            'post_message': MessageCreateSerializer,
            'reply_message': MessageReplySerializer,
            'partial_update': MessageUpdateSerializer,
        }

        return serializer_map.get(self.action, super().get_serializer_class())

    def post_message(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data,
                                         context={'request': request})
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)
        return Response(instance, status=status.HTTP_201_CREATED)

    def get_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        serializer_class = self.get_serializer_class()
        if 'context' in kwargs:
            kwargs['context'].update(self.get_serializer_context())
        else:
            kwargs['context'] = self.get_serializer_context()

        return serializer_class(*args, **kwargs)

    def perform_create(self, serializer):
        return serializer.save()

    def reply_message(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data,
                                         context={
                                             'request': request,
                                             'kwargs': kwargs,
                                         })

        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)
        return Response(MessageSerializer(instance).data,
                        status=status.HTTP_201_CREATED)
