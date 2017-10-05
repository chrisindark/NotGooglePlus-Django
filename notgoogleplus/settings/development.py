from notgoogleplus.settings.common import *
from corsheaders.defaults import default_headers

# Quick-start development settings - unsuitable for production

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'v&s0ym!t$uc^vdufh8(tpac7c*=xyu#am8e32)e1f0bnr*ys(b'

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


SITE_NAME = 'NotGooglePlus'
APP_NAME = 'NotGooglePlus'
STATIC_APP_URL = get_env_var('STATIC_APP_URL', default='http://localhost:3000')
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
    'rest_framework_swagger',
)

MIDDLEWARE = (
    'notgoogleplus.middleware.QueryCountDebugMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
) + MIDDLEWARE

DATABASES = {}

if os.environ.get('NG_HEROKU_ENV'):
    import dj_database_url
    DATABASES['default'] = dj_database_url.config(conn_max_age=500)
else:
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.mysql',
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
    'notgoogleplus.apps.accounts.authentication.JWTAuthentication',
)

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch2_backend.Elasticsearch2SearchEngine',
        'URL': 'http://127.0.0.1:9200/',
        'INDEX_NAME': 'haystack',
    },
}

REDIS_URL = 'redis://127.0.0.1:6379'

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
EMAIL_HOST = get_env_var('NG_EMAIL_HOST')
EMAIL_PORT = get_env_var('NG_EMAIL_PORT')
EMAIL_HOST_USER = get_env_var('NG_EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = get_env_var('NG_EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

SEND_ACTIVATION_EMAIL = False

ACCOUNT_ACTIVATION_URL = 'home/account/activate'
ACCOUNT_ACTIVATION_EMAIL_SUBJECT = 'account_activation_email_subject.txt'
ACCOUNT_ACTIVATION_EMAIL_BODY = 'account_activation_email_body.txt'
ACCOUNT_ACTIVATION_EMAIL_TEMPLATE = 'account_activation_email.html'

ACCOUNT_CONFIRMATION_EMAIL_SUBJECT = 'account_confirmation_email_subject.html'
ACCOUNT_CONFIRMATION_EMAIL_BODY = 'account_confirmation_email_body.html'
ACCOUNT_CONFIRMATION_EMAIL_TEMPLATE = 'account_confirmation_email.html'

PASSWORD_RESET_CONFIRM_URL = 'home/password/reset/confirm'
PASSWORD_RESET_EMAIL_SUBJECT = 'account_password_reset_subject.txt'
PASSWORD_RESET_EMAIL_BODY = 'account_password_reset_body.txt'
PASSWORD_RESET_EMAIL_TEMPLATE = 'account_password_reset_email.html'

GOOGLE_OAUTH2_CLIENT_ID = '307738501047-pnpgrstnfm2r3bmqceptf5mve28sdt3c.apps.googleusercontent.com'
GOOGLE_OAUTH2_CLIENT_SECRET = 'Lxff0ic5RSUaPccrOC3ieKZa'
GOOGLE_OAUTH2_CALLBACK_URL = 'http://127.0.0.1:3000/auth/google/callback'

TWITTER_OAUTH_CONSUMER_KEY = '1yCuO4Sfvc3IGEIvE1rPdgfaK'
TWITTER_OAUTH_CONSUMER_SECRET = 'RGjHoQB7fLcIVIUikbqMZfHqkFMff4N0wXeAUAHK1zamr2yYK8'
TWITTER_OAUTH_CALLBACK_URL = 'http://127.0.0.1:3000/auth/twitter/callback'

GITHUB_OAUTH2_CLIENT_ID = '94893b580eb207c6ffdf'
GITHUB_OAUTH2_CLIENT_SECRET = '907ad95aa39ca47bbf217bfc60e3b060a89ff40a'
GITHUB_OAUTH2_CALLBACK_URL = 'http://127.0.0.1:3000/auth/github/callback'

STRIPE_OAUTH2_CLIENT_ID = 'ca_BIg0n29mFhqx1LmMIAXEppUwUwYH4HGN'
STRIPE_OAUTH2_CLIENT_SECRET = 'sk_test_JCKVNZDXaeIgEUHMaYQGHGzu'
STRIPE_OAUTH2_CALLBACK_URL = 'http://127.0.0.1:3000/auth/stripe/callback'
STRIPE_PUBLISHABLE_KEY = 'pk_test_6T7ARIdKL2DJVFBqKNWvVbJV'

AWS_ACCESS_KEY_ID = '12345678'
AWS_SECRET_ACCESS_KEY = '12345678'
AWS_S3_HOST = 'http://127.0.0.1:4567'
AWS_STORAGE_BUCKET_NAME = 'notgoogleplus-media'
AWS_S3_USE_SSL = False
AWS_S3_DEFAULT_REGION = 'us-east-1'

AWS_SQS_HOST = 'http://127.0.0.1:4568'
AWS_SQS_DEFAULT_REGION = 'us-east-1'

# AWS_ACCESS_KEY_ID = 'AKIAJUHLRDP6V7HDH7AQ'
# AWS_SECRET_ACCESS_KEY = '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'
# AWS_S3_HOST = 'http://s3.amazonaws.com'
# AWS_STORAGE_BUCKET_NAME = 'file.upload.server'
# AWS_S3_USE_SSL = False
# AWS_S3_DEFAULT_REGION = 'us-east-1'
