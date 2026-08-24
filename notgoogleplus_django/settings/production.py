from notgoogleplus_django.settings.common import *

DEBUG = False

SECRET_KEY = get_env_var("SECRET_KEY")

DATABASES = {}
# DATABASES['default'] = {
#     'ENGINE': 'django.db.backends.mysql',
#     'NAME': get_env_var('NG_DB_NAME'),
#     'USER': get_env_var('NG_DB_USERNAME'),
#     'PASSWORD': get_env_var('NG_DB_PASSWORD'),
#     'HOST': get_env_var('NG_DB_HOST'),
#     'PORT': get_env_var('NG_DB_PORT'),
# }
# DATABASES['default'] = {
#     'ENGINE': 'django.db.backends.postgresql',
#     'NAME': get_env_var('NG_DB_NAME'),
#     'USER': get_env_var('NG_DB_USERNAME'),
#     'PASSWORD': get_env_var('NG_DB_PASSWORD'),
#     'HOST': get_env_var('NG_DB_HOST'),
#     'PORT': get_env_var('NG_DB_PORT'),
# }

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
