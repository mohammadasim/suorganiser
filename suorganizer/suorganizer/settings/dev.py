from .base import *
from ..log_filters import ManagementFilter

DEBUG = True

ALLOWED_HOSTS = ['app', '127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': get_env_variable('PGSQL_DB_NAME'),
        'USER': get_env_variable('PGSQL_DB_USER'),
        'PASSWORD': get_env_variable('PGSQL_DB_PASW'),
        'HOST': get_env_variable('PGSQL_DB_HOST'),
        'PORT': get_env_variable('PGSQL_DB_PORT')
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
