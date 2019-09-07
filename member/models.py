import os
import datetime
import hashlib
import random
import string
import uuid
import json

from django.core import validators
from django.conf import settings
from django.db import models
from django.db import transaction
from django.core.mail import send_mail

from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin,
                                        BaseUserManager)

from django.utils import timezone
from django.utils.translation import pgettext_lazy as _


class UserManager(BaseUserManager):
    """Customize the creatioin of user and super user
    """

    def _create_user(self,
                     username,
                     email,
                     password,
                     mobile_number,
                     is_staff=False,
                     is_superuser=False,
                     **kwargs):

        now = timezone.now()
        if not username:
            raise ValueError("The given username must be set")

        email = self.normalize_email(email)
        user = self.model(username=username,
                          email=email,
                          is_staff=is_staff,
                          is_active=True,
                          is_superuser=is_superuser,
                          mobile_phone=mobile_number,
                          date_joined=now,
                          **kwargs)

        user.set_password(password)

        with transaction.atomic():
            user.save(using=self._db)
            # you can create other models foreign to model User here

        return user

    def create_user(self,
                    email,
                    username='',
                    password=None,
                    mobile_number='',
                    is_staff=False,
                    is_superuser=False,
                    **kwargs):
        if username == '':
            username = email.split('@')[0]
        if password is None:
            password = ''.join(
                random.sample(string.ascii_letters + string.digits, 10))

        return self._create_user(username, email, password, mobile_number,
                                 is_staff, is_superuser, **kwargs)

    def create_superuser(self,
                         email,
                         username='',
                         password=None,
                         mobile_number='',
                         **kwargs):
        if username == '':
            username = email.split('@')[0]

        return self._create_user(username, email, password, mobile_number,
                                 True, True, **kwargs)


class AbstractUser(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    Username, password and email are required. Other fields are optional.
    """
    username = models.CharField(
        _('User field', 'username'),
        max_length=20,
        default='',
        help_text=_(
            'User field',
            'Required. 20 characters or fewer. Letters, digits and '
            '@/./+/-/_ only.'),
        validators=[
            validators.RegexValidator(
                r'^[\w.@+-]+$',
                _(
                    'User field', 'Enter a valid username. '
                    'This value may contain only letters, numbers '
                    'and @/./+/-/_ characters.'), 'invalid'),
        ])
    first_name = models.CharField(_('User field', 'first name'),
                                  max_length=30,
                                  blank=True)
    last_name = models.CharField(_('User field', 'last name'),
                                 max_length=30,
                                 blank=True)
    email = models.EmailField(_('User field', 'email address'), unique=True)
    is_staff = models.BooleanField(
        _('User field', 'staff status'),
        default=False,
        help_text=_(
            'User field',
            'Designates whether the user can log into this admin '
            'site.'))
    is_active = models.BooleanField(
        _('User field', 'active'),
        default=True,
        help_text=_(
            'User field', 'Designates whether this user should be treated as '
            'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('User field', 'date joined'),
                                       default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('User field', 'user')
        verbose_name_plural = _('User field', 'users')
        abstract = True

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)


class User(AbstractUser):
    """a customable user model
    """

    mobile_phone = models.CharField(_('User model', 'cell phone num'),
                                    max_length=32,
                                    default='')
    token = models.CharField(max_length=300, unique=True)

    object = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        if not self.token:
            for _ in range(100):
                token = uuid.uuid4().hex
                if not type(self).objects.filter(token=token).exists():
                    self.token = token
                    break

        return super().save(*args, **kwargs)


class Horoscope:
    """a simple horoscope to date mapper
    """

    @staticmethod
    def _str_to_date(date):
        date = datetime.datetime.strptime(date, '%m-%d')
        return date

    mapper = {
        'aries':
        [_str_to_date.__func__('03-21'),
         _str_to_date.__func__('04-20')],
        'taurus':
        [_str_to_date.__func__('04-21'),
         _str_to_date.__func__('05-21')],
        'gemini':
        [_str_to_date.__func__('05-22'),
         _str_to_date.__func__('06-21')],
        'cancer':
        [_str_to_date.__func__('06-22'),
         _str_to_date.__func__('07-23')],
        'leo':
        [_str_to_date.__func__('07-24'),
         _str_to_date.__func__('08-23')],
        'virgo':
        [_str_to_date.__func__('08-24'),
         _str_to_date.__func__('09-23')],
        'libra':
        [_str_to_date.__func__('09-24'),
         _str_to_date.__func__('10-23')],
        'scorpio':
        [_str_to_date.__func__('10-24'),
         _str_to_date.__func__('11-22')],
        'sagittarius':
        [_str_to_date.__func__('11-23'),
         _str_to_date.__func__('12-22')],
        'capricorn':
        [_str_to_date.__func__('12-23'),
         _str_to_date.__func__('01-20')],
        'aquarius':
        [_str_to_date.__func__('01-21'),
         _str_to_date.__func__('02-19')],
        'pisces':
        [_str_to_date.__func__('02-20'),
         _str_to_date.__func__('03-20')]
    }

    @classmethod
    def from_date(cls, date):
        result = None

        try:
            date = datetime.datetime.strptime(date, '%m-%d')
        except ValueError:
            raise ValueError('the format should be {}}'.format('%m-%d'))

        for key, value in Horoscope.mapper.items():
            if date >= value[0] and date <= value[1]:
                result = key
                break

        return result or 'capricorn'


# maybe we should define some util class or function for image process
# gray?
# compress?


class ProfileAttrProxy:
    def __init__(self, profile):
        self._profile = profile
        super().__init__()

    def __getattr__(self, item):
        data = json.loads(self._profile.extra_data or '{}')
        return data[item]

    def __setattr__(self, key, value):
        if key == '_profile':
            return super().__setattr__(key, value)

        try:
            data = json.loads(self._profile.extra_data)
        except ValueError:
            data = {}

        data[key] = value
        self._profile.extra_data = json.dumps(data)

    class Meta:
        proxy = True


class BaseProfile(models.Model):
    """
    """

    def _get_upload_path(instance, filename):
        now = timezone.now()
        year = now.strftime('%Y')
        path = instance.__class__.__name__
        folder = year

        salt = hashlib.sha1(str(
            random.random()).encode('utf-8')).hexdigest()[:8]
        ext = filename.split('.')[:-1]
        filename = '.'.join([
            hashlib.sha1((salt + filename).encode('utf-8')).hexdigest()[:15],
            ext
        ])

        return os.path.join(path, folder, instance.user.token, filename)

    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                models.CASCADE,
                                primary_key=True,
                                related_name='%(class)s',
                                verbose_name=_('baseProfile', 'user'))
    mugshot = models.ImageField(blank=True,
                                null=True,
                                upload_to=_get_upload_path,
                                verbose_name=_('baseProfile', 'mugshot'))

    def __str__(self):
        return "{}'s profile".format(self.user.username)

    class Meta:
        abstract = True


class DiamondProfile(models.Model):
    """
    """

    class Meta:
        abstract = True


class Profile(DiamondProfile, BaseProfile):
    """
    """

    class Meta:
        verbose_name = _('profile', 'member profile')

    @property
    def attrs(self):
        return ProfileAttrProxy(self)


class SocialUserData(models.Model):
    """a model for social auth
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             models.CASCADE,
                             related_name='social_ids')
    service = models.CharField(db_index=True, max_length=255)
    username = models.CharField(db_index=True, max_length=255)

    class Meta:
        unique_together = ('service', 'username')
