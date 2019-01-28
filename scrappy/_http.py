import requests

from scrappy import settings
from scrappy.exceptions import WebServerError


API_SETTINGS = getattr(settings, 'API', None)
if API_SETTINGS is None:
    raise ValueError('\'API\' setting not set.')


class WebServer:

    end_point = API_SETTINGS.ENDPOINT
    api_key = API_SETTINGS.API_KEY

    def send_payload(self, payload):
        try:
            resp = requests.post(self.end_point, json=payload,
                                 headers={'Api-Key': self.api_key},
                                 timeout=5)
            if resp.status_code != 200:
                raise WebServerError('Failed to post payload.')
        except requests.RequestException as e:
            raise WebServerError('Failed to post payload: RequestException', e)
