import requests
from bs4 import BeautifulSoup
from requests import RequestException


USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'


def fetch_html(url, timeout):
    try:
        request = requests.get(url, timeout=timeout, headers={'User-Agent': USER_AGENT})
        if request.status_code == 200:
            return request.text
    except RequestException:
        pass
    return ''


def make_soup(url):
    html = fetch_html(url, timeout=10)
    return BeautifulSoup(html, 'html.parser')
