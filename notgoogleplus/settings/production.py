from notgoogleplus.settings.common import *
from corsheaders.defaults import default_headers

DEBUG = False

SECRET_KEY = get_env_var('SECRET_KEY')

DATABASES = {
    'default': {}
}

STATIC_ROOT = os.path.abspath(os.path.join('/var/www/html/notgoogleplus/staging', STATIC_PATH))
MEDIA_ROOT = os.path.abspath(os.path.join('/var/www/html/notgoogleplus/staging', MEDIA_PATH))

CORS_ORIGIN_WHITELIST = ()
CORS_ORIGIN_ALLOW_ALL = False
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

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
