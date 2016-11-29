from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

from member.models import SocialUserData

User = get_user_model()


class Backend(ModelBackend):

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


class EmailPasswordBackend(Backend):

    """Authentication with user's email and password
    """

    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            return None

        if user.check_password(password):
            return user

class SocialLoginBackend(Backend):

    """Authentication with social service id
    """

    def authenticate(self, service=None, username=None, **kwargs):
        try:
            user_data = SocialUserData.objects.get(service=service, username=username)

            return user_data.user
        except SocialUserData.DoesNotExist:
            return None
