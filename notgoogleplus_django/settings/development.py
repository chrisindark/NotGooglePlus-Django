import os

from corsheaders.defaults import default_headers

from notgoogleplus_django.settings.common import *

# load environment variables from .env file
read_env("development")


# Quick-start development settings - unsuitable for production

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_env_var("SECRET_KEY", default="secret-key")

ALLOWED_HOSTS = (
    "localhost",
    "0.0.0.0",
    "127.0.0.1",
    "dev.notgoogleplus.com",
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = get_env_var("DEBUG", False)

APPEND_SLASH = True

LOGGING["loggers"]["django.db"]["level"] = "DEBUG"


SITE_NAME = "NotGooglePlus"
APP_NAME = "NotGooglePlus"
STATIC_APP_URL = get_env_var("STATIC_APP_URL", default="http://localhost:8000/")
DOMAIN_URL = STATIC_APP_URL.split("://")[1]
LOGIN_URL = "/api-auth/login/"
LOGOUT_URL = "/api-auth/logout/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

# SWAGGER SETTINGS
SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "api_key": {"type": "apiKey", "in": "header", "name": "Authorization"},
        "permission_denied_handler": "django.contrib.auth.views.login",
        "is_authenticated": True,  # Set to True to enforce user authentication,
        "is_superuser": True,  # Set to True to enforce admin only access
    }
}

INSTALLED_APPS += (
    "django_extensions",
    "debug_toolbar",
    # "compressor",
)

SHELL_PLUS_PRINT_SQL = (
    True  # Automatically prints SQL queries in shell_plus without the flag
)

MIDDLEWARE = (
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    # 'notgoogleplus_django.middleware.QueryCountDebugMiddleware',
) + MIDDLEWARE

# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

DATABASES = {}
DATABASES["default"] = {
    "ENGINE": "django.db.backends.sqlite3",
    "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
}

STATIC_ROOT = os.path.abspath(os.path.join(PROJECT_PATH, STATIC_PATH))
MEDIA_ROOT = os.path.abspath(os.path.join(PROJECT_PATH, MEDIA_PATH))

CORS_ORIGIN_WHITELIST = ()
CORS_ORIGIN_ALLOW_ALL = True
CORS_EXPOSE_HEADERS = (
    "Access-Control-Allow-Origin",
    "Content-Disposition",
    "Content-Type",
    "Content-Length",
    "Notgoogleplus-App-Version",
)
CORS_ALLOW_HEADERS = default_headers + ("Content-Disposition",)

SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "http")

# EMAIL SETTINGS
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = get_env_var('NG_EMAIL_HOST', default='smtp.gmail.com')
# EMAIL_PORT = get_env_var('NG_EMAIL_PORT', default=587)
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = get_env_var('NG_EMAIL_HOST_USER', default='admin@gmail.com')
# EMAIL_HOST_PASSWORD = get_env_var('NG_EMAIL_HOST_PASSWORD', default='password')
# DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

SEND_ACTIVATION_EMAIL = False

ACCOUNT_ACTIVATION_URL = "account/activate"
ACCOUNT_ACTIVATION_EMAIL_SUBJECT = "account_activation_email_subject.txt"
ACCOUNT_ACTIVATION_EMAIL_BODY = "account_activation_email_body.txt"
ACCOUNT_ACTIVATION_EMAIL_TEMPLATE = "account_activation_email.html"

ACCOUNT_CONFIRMATION_EMAIL_SUBJECT = "account_confirmation_email_subject.html"
ACCOUNT_CONFIRMATION_EMAIL_BODY = "account_confirmation_email_body.html"
ACCOUNT_CONFIRMATION_EMAIL_TEMPLATE = "account_confirmation_email.html"

PASSWORD_RESET_CONFIRM_URL = "password/reset/confirm"
PASSWORD_RESET_EMAIL_SUBJECT = "account_password_reset_subject.txt"
PASSWORD_RESET_EMAIL_BODY = "account_password_reset_body.txt"
PASSWORD_RESET_EMAIL_TEMPLATE = "account_password_reset_email.html"


REDIS_HOST = get_env_var("NG_REDIS_HOST", "127.0.0.1")
REDIS_PORT = get_env_var("NG_REDIS_PORT", "6379")
REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}"

# CACHE SETTINGS
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

AWS_ACCESS_KEY_ID = get_env_var("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = get_env_var("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = get_env_var("AWS_STORAGE_BUCKET_NAME")
AWS_S3_DEFAULT_REGION = get_env_var("AWS_S3_DEFAULT_REGION")
AWS_S3_HOST = get_env_var("AWS_S3_HOST")
AWS_S3_PORT = get_env_var("AWS_S3_PORT")
AWS_S3_ENDPOINT_URL = get_env_var("AWS_S3_ENDPOINT_URL")
AWS_S3_USE_SSL = get_env_var("AWS_S3_USE_SSL", False)

DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

# CELERY SETTINGS
# CELERY_BROKER_URL = REDIS_URL
# CELERY_RESULT_BACKEND = REDIS_URL
# CELERY_ACCEPT_CONTENT = ['json']
# CELERY_TASK_SERIALIZER = 'json'
# CELERY_RESULT_SERIALIZER = 'json'
# CELERY_TIMEZONE = 'UTC'
# CELERY_TASK_CREATE_MISSING_QUEUES = True
# CELERYD_PREFETCH_MULTIPLIER = 1
# CELERY_IGNORE_RESULT = True
# CELERYD_TASK_SOFT_TIME_LIMIT = 300

# HAYSTACK_CONNECTIONS = {
#     'default': {
#         'ENGINE': 'haystack.backends.elasticsearch2_backend.Elasticsearch2SearchEngine',
#         'URL': 'http://127.0.0.1:9200/',
#         'INDEX_NAME': 'haystack',
#     },
# }

# CHANNEL SETTINGS
# CHANNEL_LAYERS = {
#     'default': {
#         'BACKEND': 'asgi_redis.RedisChannelLayer',
#         'CONFIG': {
#             'hosts': [REDIS_URL],
#         },
#         'ROUTING': 'notgoogleplus.routing.channel_routing',
#     }
# }

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

# AWS_SQS_HOST = get_env_var('AWS_SQS_HOST')
# AWS_SQS_DEFAULT_REGION = get_env_var('AWS_SQS_DEFAULT_REGION')
