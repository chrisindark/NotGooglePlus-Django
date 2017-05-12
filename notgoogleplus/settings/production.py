from notgoogleplus.settings.common import *
import dj_database_url

DEBUG = False

SECRET_KEY = get_env_var('SECRET_KEY')

DATABASES = {
    'default': dj_database_url.config()
}

CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = ()
