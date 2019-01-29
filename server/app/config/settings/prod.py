import logging

import sentry_sdk
from django.utils.log import DEFAULT_LOGGING
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import LoggingIntegration

from .base import *


# DEBUG CONFIGURATION
# ------------------------------------------------------------------------------
DEBUG = False


# SENTRY SDK
# ------------------------------------------------------------------------------
sentry_logging = LoggingIntegration(
    level=logging.INFO,        # Capture info and above as breadcrumbs
    event_level=logging.ERROR  # Send errors as events
)

sentry_sdk.init(
    dsn=config('SENTRY_DSN'),
    integrations=[sentry_logging, DjangoIntegration()],
)


# DJANGO CORS HEADERS
# ------------------------------------------------------------------------------
CORS_ORIGIN_ALLOW_ALL = True


# LOGGING CONFIGURATION
# ------------------------------------------------------------------------------
LOG_LEVEL = config('DJANGO_LOG_LEVEL', default='info').upper()
LOGGING_CONFIG = None
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        },
        'django.server': DEFAULT_LOGGING['formatters']['django.server'],
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console',
        },
        'django.server': DEFAULT_LOGGING['handlers']['django.server'],
        'sentry': {
            'level': 'WARNING',
            'class': 'sentry_sdk.integrations.logging.SentryHandler',
        },
    },
    'loggers': {
        '': {
            'level': 'WARNING',
            'handlers': ['console', 'sentry'],
        },
        'django.server': DEFAULT_LOGGING['loggers']['django.server'],
        'app': {
            'level': LOG_LEVEL,
            'handlers': ['console', 'sentry'],
            'propagate': False,
        },
    },
}
