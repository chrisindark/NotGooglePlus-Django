"""
Django settings for notgoogleplus project.

Generated by 'django-admin startproject' using Django 1.10.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
import dj_database_url
from django.core.exceptions import ImproperlyConfigured

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',

    'notgoogleplus.apps.core',
    'notgoogleplus.apps.accounts',
    'notgoogleplus.apps.profiles',
    'notgoogleplus.apps.posts',
    'notgoogleplus.apps.articles',
)

MIDDLEWARE = (
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'notgoogleplus.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'notgoogleplus.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

MEDIA_PATH = 'media/'
STATIC_PATH = 'static/'

STATIC_ROOT = os.path.abspath(os.path.join(BASE_DIR, STATIC_PATH))
MEDIA_ROOT = os.path.abspath(os.path.join(BASE_DIR, MEDIA_PATH))

STATICFILES_DIRS = []

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'compressor.finders.CompressorFinder',
    )

# COMPRESS_ENABLED = os.environ.get('COMPRESS_ENABLED', False)

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'PAGE_SIZE': 5
}

AUTH_USER_MODEL = 'accounts.Account'
AUTHENTICATION_BACKENDS = ('notgoogleplus.apps.accounts.backends.UsernameOrEmailBackend',)

#SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

LOGGING = {
    'disable_existing_loggers': False,
    'version': 1,
    'formatters': {
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG', # message level to be written to console
            # logging handler that outputs log messages to terminal
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        '': {
            # this sets root level logger to log debug and higher level
            # logs to console. All other loggers inherit settings from
            # root level logger.
            'handlers': ['console'],
            'level': 'DEBUG',
            # this tells logger to send logging message
            # to its parent (will send if set to True)
            'propagate': False
        },
        'django.db': {
            # 'level': 'DEBUG'
            # django also has database level logging
        },
    },
}


def get_env_var(name, default=None):
    try:
        return os.environ[name]
    except KeyError:
        if default:
            return default
        raise ImproperlyConfigured('Set the {0} environment variable.'.format(name))

SECRET_KEY = 'v&s0ym!t$uc^vdufh8(tpac7c*=xyu#am8e32)e1f0bnr*ys(b'

DEBUG = True

# SWAGGER SETTINGS
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'api_key': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization'
        }
    }
}

INSTALLED_APPS += (
    'django_extensions',
    'rest_framework_swagger'
)

MIDDLEWARE = ('notgoogleplus.middleware.QueryCountDebugMiddleware',) + MIDDLEWARE

DATABASES = {}
DATABASES['default'] = dj_database_url.config(conn_max_age=500)

ALLOWED_HOSTS = (
    'ancient-tor-16694.herokuapp.com',
    '0.0.0.0'
)

CORS_ORIGIN_ALLOW_ALL = True

PASSWORD_RESET_CONFIRM_URL = '#/password/reset/confirm'
PASSWORD_RESET_EMAIL_SUBJECT = 'account_password_reset_subject.txt'
PASSWORD_RESET_EMAIL_TEMPLATE = 'account_password_reset_email.html'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# EMAIL SETTINGS
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'abc123abc123xyz123@gmail.com'
EMAIL_HOST_PASSWORD = 'abccababccab'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

FILE_UPLOAD_PATH = 'uploads/'
