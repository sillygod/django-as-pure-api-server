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
                    raise serializers.ValidationError(msg)

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
            raise serializers.ValidationError(msg)


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
            raise serializers.ValidationError({'code': 1001,
                                               'msg': 'this email has been registered'})
        return value

    def validate_password2(self, value):
        if value != self.initial_data['password']:
            raise serializers.ValidationError({'code': 1002, 'msg': 'password is not consistent'})

    def create(self, validated_data):
        validated_data.pop('password2')
        instance = User.objects.create_user(**validated_data)
        return instance


class UserSerializerNew(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email', )

