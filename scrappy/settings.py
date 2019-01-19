from decouple import config


# Set to True if you want urls that failed to be scrapped to be scrapped again
# on the next request.
RETRY_FAILED_URLS = False


PRODUCTION = config('PRODUCTION', False)
