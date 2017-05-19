from notgoogleplus.settings.common import *

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'v&s0ym!t$uc^vdufh8(tpac7c*=xyu#am8e32)e1f0bnr*ys(b'

ALLOWED_HOSTS = (
    'localhost',
    '127.0.0.1',
    'ancient-tor-16694.herokuapp.com',
)

# SECURITY WARNING: don't run with debug turned on in production!
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

if os.environ.get('NG_HEROKU_ENV'):
    DATABASES['default'] = dj_database_url.config(conn_max_age=500)
else:
    DATABASES['default'] = {
        'NAME': 'notgoogleplus',
        'ENGINE': 'django.db.backends.mysql',
        'USER': get_env_var('NG_DB_USERNAME'),
        'PASSWORD': get_env_var('NG_DB_PASSWORD'),
        'HOST': get_env_var('NG_DB_HOST'),
        'PORT': get_env_var('NG_DB_PORT'),
    }

CORS_ORIGIN_WHITELIST = ()
CORS_ORIGIN_ALLOW_ALL = True

# CHANNEL_LAYERS = {
#     'default': {
#         'BACKEND': 'asgi_redis.RedisChannelLayer',
#         'CONFIG': {
#             'hosts': [REDIS_URL],
#         },
#         'ROUTING': 'notgoogleplus.routing.channel_routing',
#     }
# }

# CELERY SETTINGS
BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Kolkata'

PASSWORD_RESET_CONFIRM_URL = '#/password/reset/confirm'
PASSWORD_RESET_EMAIL_SUBJECT = 'account_password_reset_subject.txt'
PASSWORD_RESET_EMAIL_TEMPLATE = 'account_password_reset_email.html'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# EMAIL SETTINGS
# EMAIL_USE_TLS = True
# EMAIL_HOST = get_env_var('NG_EMAIL_HOST')
# EMAIL_PORT = get_env_var('NG_EMAIL_PORT')
# EMAIL_HOST_USER = get_env_var('NG_EMAIL_HOST_USER')
# EMAIL_HOST_PASSWORD = get_env_var('NG_EMAIL_HOST_PASSWORD')
# DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

FILE_UPLOAD_PATH = 'uploads/'
