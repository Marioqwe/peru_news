from decouple import config


API = {
    'API_KEY': config('API_KEY'),
}


PRODUCTION = config('PRODUCTION', default=False, cast=bool)


REDIS = {
    'HOST': config('REDIS_HOST'),
    'PASSWORD': config('REDIS_PASSWORD'),
    'PORT': config('REDIS_PORT'),
}


# Set to True if you want urls that failed to be scrapped to be scrapped again
# on the next request.
RETRY_FAILED_URLS = False
