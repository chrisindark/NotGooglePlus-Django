from notgoogleplus.settings.common import *
import dj_database_url

DEBUG = False

SECRET_KEY = get_env_var('SECRET_KEY')

DATABASES = {
    'default': dj_database_url.config()
}

CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = ()

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
