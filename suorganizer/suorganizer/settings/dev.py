from .base import *
from ..log_filters import ManagementFilter
import socket

DEBUG = True

ALLOWED_HOSTS = ['app', '127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': get_env_variable('PGSQL_DB_NAME'),
        'USER': get_env_variable('PGSQL_DB_USER'),
        'PASSWORD': get_env_variable('PGSQL_DB_PASW'),
        'HOST': get_env_variable('PGSQL_DB_HOST'),
        'PORT': get_env_variable('PGSQL_DB_PORT'),
        # 'OPTIONS': {'sslmode': 'verify-full'},
    }
}
# Dev email settings, enables email output to the console
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
SERVER_EMAIL = 'contact@django-unleashed.com'
DEFAULT_FROM_EMAIL = 'no-reply@django-unleashed.com'
EMAIL_SUBJECT_PREFIX = '[Startup Organizer]'
MANAGERS = (
    ('Us', 'ourselves@django-unleashed.com'),
)
SITE_ID = 1
# Auth app settings
# Redirect to blogs_post_list view
LOGIN_REDIRECT_URL = 'blogs_posts_list'
LOGIN_URL = 'dj-auth:login'
# Logger settings
verbose = (
    "[%(asctime)s] %(levelname)s"
    "[%(name)s:%(lineno)s] %(message)s"
)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'remove_migration_sql': {
            '()': ManagementFilter
        },
    },
    'handlers': {
        'console': {
            'filters': ['remove_migration_sql'],
            'class': 'logging.StreamHandler',
        },
    },
    'formatters': {
        'verbose': {
            'format': verbose,
            'datefmt': "%Y-%b-%d %H:%M:%S"
        },

    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'formatter': 'verbose'
        }

    }
}

# django-debug-toolbar
INSTALLED_APPS += ('debug_toolbar',)
MIDDLEWARE += ()
socket_hostname = socket.gethostname()
container_ip = socket.gethostbyname(socket_hostname)
INTERNAL_IPS = [container_ip]


def show_toolbar(request):
    return True


DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': show_toolbar,
}

# Cache settings
"""
We use local memory cache, which simply keeps webpages
in memory. In deployment this setting will be changed.
It is possible to define multiple different caches, each of
which might fulfill a different purpose. Here we simply
define a single cache and called it default.
The BACKEND key tells the cache what kind of cache it is, while
the location gives the cache a unique identifier, used separately
from the name default. We also set how long we want the cache to
remember webpages.
By defining the CACHE_MIDDLEWARE_ALIAS we tell the middleware
which cache to use.
"""
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
        'TIMEOUT': 600,  # seconds == 10 minutes
    }
}
CACHE_MIDDLEWARE_ALIAS = 'default'
"""
As the order of the middleware in response is
from bottom to top of the MIDDLEWARE list we
put updatecachemiddleware at the top so it is called 
last.
"""
MIDDLEWARE = ('django.middleware.cache.UpdateCacheMiddleware',) \
             + MIDDLEWARE \
             + ('django.middleware.cache.FetchFromCacheMiddleware',)
