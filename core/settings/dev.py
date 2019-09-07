"""
a base settings for dev, prod

here, we can check django-environ
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from .base import *  # pylint: disable=W0614
# above comment can disable pylint waring for this line

# NOTE: this is just convenient for dev use, you must specify the
# domain you want to bypass.
CORS_ORIGIN_ALLOW_ALL = True

INSTALLED_APPS += (
    'debug_toolbar',
    'django_extensions',
)

MIDDLEWARE += (
    # thrid party middleware
    'debug_toolbar.middleware.DebugToolbarMiddleware', )

ROOT_URLCONF = 'core.urls'

WSGI_APPLICATION = 'core.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

GRAPPELLI_ADMIN_TITLE = 'demo-project'

AUTHENTICATION_BACKENDS = (
    'member.backends.EmailPasswordBackend',
    'member.backends.SocialLoginBackend',
)

REST_FRAMEWORK = {
    'DEFAULT_VERSIONING_CLASS':
    'rest_framework.versioning.URLPathVersioning',
    'DEFAULT_PERMISSION_CLASSES':
    ('rest_framework.permissions.IsAuthenticated', ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_SCHEMA_CLASS':
    'rest_framework.schemas.coreapi.AutoSchema',
    'EXCEPTION_HANDLER':
    'api.utils.api_error_handler',
}

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'


def show_toolbar(request):
    """we can write some logic for whether toolbar should appear or not"""
    return True


DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": show_toolbar,
}

DEBUG_TOOLBAR_PANELS = [
    # TODO: look up this
    # 'ddt_request_history.panels.request_history.RequestHistoryPanel',
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
]
