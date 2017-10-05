from notgoogleplus.settings.common import *

# Quick-start development settings - unsuitable for production

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'v&s0ym!t$uc^vdufh8(tpac7c*=xyu#am8e32)e1f0bnr*ys(b'

ALLOWED_HOSTS = (
    'dev.ngp.server.com',
    'ancient-tor-16694.herokuapp.com',
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

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

LOGIN_URL = '/api-auth/login/'
LOGOUT_URL = '/api-auth/logout/'
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
    'rest_framework_swagger',
)

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

STATIC_ROOT = os.path.abspath(os.path.join('/var/www/html/notgoogleplus/staging', STATIC_PATH))
MEDIA_ROOT = os.path.abspath(os.path.join('/var/www/html/notgoogleplus/staging', MEDIA_PATH))

CORS_ORIGIN_WHITELIST = ()
CORS_ORIGIN_ALLOW_ALL = True
CORS_EXPOSE_HEADERS = (
    'Access-Control-Allow-Origin',
    'Content-Type',
    'Content-Length',
    'App-Version',
)

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

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
BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'
