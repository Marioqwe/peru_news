from decouple import config


API = {
    'ENDPOINT': config('API_ENDPOINT'),
    'API_KEY': config('API_KEY'),
}


# Set to True if you want urls that failed to be scrapped to be scrapped again
# on the next request.
RETRY_FAILED_URLS = False


PRODUCTION = config('PRODUCTION', False)
