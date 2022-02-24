from corsheaders.defaults import default_headers
from notgoogleplus.settings.common import *


# load environment variables from .env file
read_env(".development")


# Quick-start development settings - unsuitable for production

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_env_var('SECRET_KEY', default='secret-key')

ALLOWED_HOSTS = (
    'localhost',
    '0.0.0.0',
    '127.0.0.1',
    '172.16.9.234',
    '192.168.1.104',
    'dev.notgoogleplus.com',
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

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
            'level': 'DEBUG',  # message level to be written to console
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


SITE_NAME = 'NotGooglePlus'
APP_NAME = 'NotGooglePlus'
STATIC_APP_URL = get_env_var(
    'STATIC_APP_URL', default='http://localhost:8000/')
DOMAIN_URL = STATIC_APP_URL.split('://')[1]
LOGIN_URL = '/api-auth/login/'
LOGOUT_URL = '/api-auth/logout/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# SWAGGER SETTINGS
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'api_key': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization'
        },
        'permission_denied_handler': 'django.contrib.auth.views.login',
        'is_authenticated': True,  # Set to True to enforce user authentication,
        'is_superuser': True  # Set to True to enforce admin only access
    }
}

INSTALLED_APPS += (
    'django_extensions',
    'debug_toolbar',
    'drf_yasg',
)

MIDDLEWARE = (
    'notgoogleplus.middleware.QueryCountDebugMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
) + MIDDLEWARE

DATABASES = {}
# DATABASES['default'] = {
#     'ENGINE': 'django.db.backends.sqlite3',
#     'NAME': os.path.join(BASE_DIR, 'db.sqlite3')
# }
# DATABASES['default'] = {
#     'ENGINE': 'django.db.backends.mysql',
#     'NAME': get_env_var('NG_DB_NAME'),
#     'USER': get_env_var('NG_DB_USERNAME'),
#     'PASSWORD': get_env_var('NG_DB_PASSWORD'),
#     'HOST': get_env_var('NG_DB_HOST'),
#     'PORT': get_env_var('NG_DB_PORT'),
# }
DATABASES['default'] = {
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': get_env_var('NG_DB_NAME'),
    'USER': get_env_var('NG_DB_USERNAME'),
    'PASSWORD': get_env_var('NG_DB_PASSWORD'),
    'HOST': get_env_var('NG_DB_HOST'),
    'PORT': get_env_var('NG_DB_PORT'),
}


STATIC_ROOT = os.path.abspath(os.path.join(PROJECT_PATH, STATIC_PATH))
MEDIA_ROOT = os.path.abspath(os.path.join(PROJECT_PATH, MEDIA_PATH))

CORS_ORIGIN_WHITELIST = ()
CORS_ORIGIN_ALLOW_ALL = True
CORS_EXPOSE_HEADERS = (
    'Access-Control-Allow-Origin',
    'Content-Disposition',
    'Content-Type',
    'Content-Length',
    'App-Version',
)
CORS_ALLOW_HEADERS = default_headers + (
    'Content-Disposition',
)

SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'http')

REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'] = (
    'rest_framework.authentication.SessionAuthentication',
    'rest_framework.authentication.TokenAuthentication',
    'apps.accounts.authentication.JWTAuthentication',
)

# HAYSTACK_CONNECTIONS = {
#     'default': {
#         'ENGINE': 'haystack.backends.elasticsearch2_backend.Elasticsearch2SearchEngine',
#         'URL': 'http://127.0.0.1:9200/',
#         'INDEX_NAME': 'haystack',
#     },
# }

REDIS_HOST = "localhost"
REDIS_PORT = "6379"
REDIS_URL = 'redis://{0}:{1}'.format(REDIS_HOST, REDIS_PORT)

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'asgi_redis.RedisChannelLayer',
        'CONFIG': {
            'hosts': [REDIS_URL],
        },
        'ROUTING': 'notgoogleplus.routing.channel_routing',
    }
}

# CELERY SETTINGS
BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'

# EMAIL SETTINGS
EMAIL_USE_TLS = True
# EMAIL_HOST = get_env_var('NG_EMAIL_HOST')
# EMAIL_PORT = get_env_var('NG_EMAIL_PORT')
# EMAIL_HOST_USER = get_env_var('NG_EMAIL_HOST_USER')
# EMAIL_HOST_PASSWORD = get_env_var('NG_EMAIL_HOST_PASSWORD')
# DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

SEND_ACTIVATION_EMAIL = False

ACCOUNT_ACTIVATION_URL = STATIC_APP_URL + 'home/account/activate'
ACCOUNT_ACTIVATION_EMAIL_SUBJECT = 'account_activation_email_subject.txt'
ACCOUNT_ACTIVATION_EMAIL_BODY = 'account_activation_email_body.txt'
ACCOUNT_ACTIVATION_EMAIL_TEMPLATE = 'account_activation_email.html'

ACCOUNT_CONFIRMATION_EMAIL_SUBJECT = 'account_confirmation_email_subject.html'
ACCOUNT_CONFIRMATION_EMAIL_BODY = 'account_confirmation_email_body.html'
ACCOUNT_CONFIRMATION_EMAIL_TEMPLATE = 'account_confirmation_email.html'

PASSWORD_RESET_CONFIRM_URL = STATIC_APP_URL + 'home/password/reset/confirm'
PASSWORD_RESET_EMAIL_SUBJECT = 'account_password_reset_subject.txt'
PASSWORD_RESET_EMAIL_BODY = 'account_password_reset_body.txt'
PASSWORD_RESET_EMAIL_TEMPLATE = 'account_password_reset_email.html'

# GOOGLE_OAUTH2_CLIENT_ID = get_env_var('GOOGLE_OAUTH2_CLIENT_ID')
# GOOGLE_OAUTH2_CLIENT_SECRET = get_env_var('GOOGLE_OAUTH2_CLIENT_SECRET')
# GOOGLE_OAUTH2_CALLBACK_URL = STATIC_APP_URL + 'auth/google/callback'

# TWITTER_OAUTH_CONSUMER_KEY = get_env_var('TWITTER_OAUTH_CONSUMER_KEY')
# TWITTER_OAUTH_CONSUMER_SECRET = get_env_var('TWITTER_OAUTH_CONSUMER_SECRET')
# TWITTER_OAUTH_CALLBACK_URL = STATIC_APP_URL + 'auth/twitter/callback'

# GITHUB_OAUTH2_CLIENT_ID = get_env_var('GITHUB_OAUTH2_CLIENT_ID')
# GITHUB_OAUTH2_CLIENT_SECRET = get_env_var('GITHUB_OAUTH2_CLIENT_SECRET')
# GITHUB_OAUTH2_CALLBACK_URL = STATIC_APP_URL + 'auth/github/callback'

# STRIPE_OAUTH2_CLIENT_ID = get_env_var('STRIPE_OAUTH2_CLIENT_ID')
# STRIPE_OAUTH2_CLIENT_SECRET = get_env_var('STRIPE_OAUTH2_CLIENT_SECRET')
# STRIPE_OAUTH2_CALLBACK_URL = STATIC_APP_URL + 'auth/stripe/callback'
# STRIPE_PUBLISHABLE_KEY = get_env_var('STRIPE_PUBLISHABLE_KEY')

# AWS_ACCESS_KEY_ID = get_env_var('AWS_ACCESS_KEY_ID')
# AWS_SECRET_ACCESS_KEY = get_env_var('AWS_SECRET_ACCESS_KEY')

# AWS_S3_HOST = get_env_var('AWS_S3_HOST')
# AWS_STORAGE_BUCKET_NAME = get_env_var('AWS_STORAGE_BUCKET_NAME')
# AWS_S3_USE_SSL = False
# AWS_S3_DEFAULT_REGION = get_env_var('AWS_S3_DEFAULT_REGION')

# AWS_SQS_HOST = get_env_var('AWS_SQS_HOST')
# AWS_SQS_DEFAULT_REGION = get_env_var('AWS_SQS_DEFAULT_REGION')
