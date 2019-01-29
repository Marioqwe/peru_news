import requests

from scrappy import settings
from scrappy.exceptions import WebServerError


API_SETTINGS = getattr(settings, 'API', None)
if API_SETTINGS is None:
    raise ValueError('\'API\' setting not set.')

API_KEY = API_SETTINGS.get('API_KEY')

PRODUCTION = getattr(settings, 'PRODUCTION')
if PRODUCTION:
    API_ENDPOINT = 'https://api.perunews.xyz/v1/articles/'
else:
    API_ENDPOINT = 'http://localhost:8000/v1/articles/'


class WebServer:

    def __init__(self):
        self._timeout = 15

    def send_payload(self, payload):
        try:
            resp = requests.post(API_ENDPOINT, json=payload,
                                 headers={'Api-Key': API_KEY},
                                 timeout=self._timeout)
            if resp.status_code != 201:
                raise WebServerError('Failed to post payload.')
        except requests.RequestException as e:
            raise WebServerError('Failed to post payload: RequestException', e)
