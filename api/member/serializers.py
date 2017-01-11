from base64 import b64decode
import re
import jwt
import copy
import importlib

from django.contrib.auth import (
    get_user_model,
    authenticate
)

from django.core.files.base import ContentFile
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext as _
from rest_framework import serializers

from rest_framework_jwt.compat import (
    Serializer,
    get_username_field,
    PasswordField
)
from rest_framework_jwt.settings import api_settings
from rest_framework.relations import RelatedField
from rest_framework.settings import APISettings

from .oauth2_client import get_local_host
from .models import SocialUserData

User = get_user_model()
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
jwt_get_username_from_payload = api_settings.JWT_PAYLOAD_GET_USERNAME_HANDLER


class ForeignKeyRelatedField(RelatedField):

    """you can customize the field name to filter the result
    """

    def __init__(self, **kwargs):
        self.fname = kwargs.pop('fname', None)
        super().__init__(**kwargs)

    def to_internal_value(self, data):
        try:
            if self.name:
                filter_kwargs = {self.fname: data}
                return self.get_queryset().get(**filter_kwargs)
            else:
                return self.get_queryset().get(pk=data)

        except ObjectDoesNotExist:
            self.fail('does_not_exist', pk_value=data)
        except (TypeError, ValueError):
            self.fail('incorrect_type', data_type=type(data).__name__)

    def to_representation(self, value):
        if self.fname:
            return getattr(value, self.fname)
        else:
            return value.pk


class JSONWebTokenSerializerWithEmail(Serializer):

    """a customize jwt serializer use email and password.

    In credentials, we still need to user username because 
    """

    def __init__(self, *args, **kwargs):
        """
        Dynamically add the USERNAME_FIELD to self.fields.
        """
        super().__init__(*args, **kwargs)

        self.fields[self.username_field] = serializers.CharField()
        self.fields['password'] = PasswordField(write_only=True)

    @property
    def username_field(self):
        return get_username_field()

    def validate(self, attrs):
        credentials = {
            'username': attrs.get(self.username_field),
            'password': attrs.get('password')
        }

        if all(credentials.values()):
            user = authenticate(**credentials)

            if user:
                if not user.is_active:
                    msg = _('User account is disabled.')
                    raise serializers.ValidationError(msg, 1000)

                payload = jwt_payload_handler(user)

                return {
                    'token': jwt_encode_handler(payload),
                    'user': user
                }
            else:
                msg = _('Unable to login with provided credentials.')
                raise serializers.ValidationError(msg)
        else:
            msg = _('Must include "{username_field}" and "password".')
            msg = msg.format(username_field=self.fields['email'])
            raise serializers.ValidationError(msg, 1000)


class UserCreateSerializer(serializers.ModelSerializer):

    """handle user creation validation
    """

    password = serializers.CharField(max_length=20, min_length=6,
                                     error_messages={
                                         'blank': 'password can not be empty',
                                         'min_length': 'password is too short'})
    password2 = serializers.CharField()

    class Meta:
        model = get_user_model()
        fields = ('id', 'username')

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('this email has been registered', 1004)
        return value

    def validate_password2(self, value):
        if value != self.initial_data['password']:
            raise serializers.ValidationError('password is not consistent', 1001)

    def create(self, validated_data):
        validated_data.pop('password2')
        instance = User.objects.create_user(**validated_data)
        return instance


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('token', 'username', 'email', )


class SocialAuthSerializer(serializers.Serializer):

    """encapsulate social auth process
    """

    service = serializers.CharField(max_length=256)
    access_token = serializers.CharField(max_length=1024)

    def _service_factory(self, name):
        try:
            module = importlib.import_module('member.oauth2_client')
            service = getattr(module, name.capitalize()+'Client')
            return service
        except:
            return None

    def validate_access_token(self, value):
        """
        """
        service_class = self.validate_service(self.initial_data['service'])
        self.service_client = service_class(local_host=get_local_host(self.context['request']))
        self.service_client.set_access_token(value)
        try:
            self._social_data = self.service_client.get_user_info()
        except Exception as e:
            raise serializers.ValidationError(str(e), 1003)

        user = User.objects.filter(email=self._social_data['email'])
        if user.existst():
            social_id = SocialUserData.objects.filter(user=user.first())
            if social_id.exists():
                raise serializers.ValidationError('this email has been registered in social auth', 1002)

        return value

    def validate_service(self, value):
        """check whether the service is supported or not.
        return the service if it's supported
        """
        service = self._service_factory(value)
        if not service:
            raise serializers.ValidationError('{} social auth not supported currently'.format(value), 1008)

        return service

    def create(self, validated_data):
        """maybe user is registered but not create its own social auth account so
        we need to do a check first

        return an instance with social data and user
        """
        user = User.objects.filter(email=self._social_data['email'])
        if user.exists():
            user = user.first()
        else:
            user = User.objects.create_user(email=self._social_data['email'])

        instance = SocialUserData.objects.create(
            user=user,
            service=validated_data['service'].service.lowser(),
            username=self._social_data['id']
        )

        self._social_data.update({'user': user})
        return self._social_data

