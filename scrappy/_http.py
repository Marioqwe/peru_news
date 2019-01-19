import requests
from decouple import config

from scrappy.exceptions import WebServerError


class WebServer:

    end_point = config('API_ENDPOINT')
    api_key = config('API_KEY')

    def send_payload(self, payload):
        try:
            resp = requests.post(self.end_point, json=payload,
                                 headers={'Api-Key': self.api_key},
                                 timeout=5)
            if resp.status_code != 200:
                raise WebServerError('Failed to post payload.')
        except requests.RequestException as e:
            raise WebServerError('Failed to post payload: RequestException', e)
