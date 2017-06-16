import os
from django.core.exceptions import ImproperlyConfigured
import dj_database_url
from dotenv import load_dotenv

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_PATH = os.path.abspath(os.path.dirname(__name__))

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
    #'haystack',

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
    'notgoogleplus.middleware.AppVersionMiddleware',
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


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

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
    'EXCEPTION_HANDLER': 'notgoogleplus.apps.core.exceptions.custom_exception_handler',
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20
}

AUTH_USER_MODEL = 'accounts.Account'
AUTHENTICATION_BACKENDS = ('notgoogleplus.apps.accounts.backends.UsernameOrEmailBackend',)

#HAYSTACK_CONNECTIONS = {
    #'default': {
        #'ENGINE': 'haystack.backends.elasticsearch2_backend.Elasticsearch2SearchEngine',
        #'URL': 'http://127.0.0.1:9200/',
        #'INDEX_NAME': 'haystack',
    #},
#}


def get_env_var(name, default=None):
    try:
        return os.environ[name]
    except KeyError:
        if default:
            return default
        raise ImproperlyConfigured('Set the {0} environment variable.'.format(name))


def read_env():
    dotenv_path = os.path.join(BASE_DIR, '.env')
    try:
        load_dotenv(dotenv_path)
    except IOError:
        raise
        pass


# load environment variables from .env file
read_env()
