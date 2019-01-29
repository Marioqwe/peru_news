import datetime
import json
import pytz
import re
import traceback
from html import unescape

from scrappy import settings
from scrappy._http import WebServer
from scrappy.db import RedisManager
from scrappy.exceptions import WebServerError
from scrappy.scrappers.base import Scrapper
from scrappy.utils import make_soup


RETRY_FAILED_URLS = getattr(settings, 'RETRY_FAILED_URLS', False)


class RPP(Scrapper):

    id_ = 'rpp'
    name = 'RPP Noticias'

    BASE_URL = 'http://www.rpp.pe'
    SECTIONS = ('politica', 'mundo', 'economia', 'actualidad', 'deportes',
                'entretenimiento', 'tecnologia', 'ciencia')

    def __init__(self, logger):
        self.logger = logger
        self.webserver = WebServer()

    def _scrap_article(self, loc, section):
        target_url = self.BASE_URL + loc
        self.logger.info('|---\t%s', target_url)

        prev_failed = RedisManager.get(target_url)
        if prev_failed is not None:
            if prev_failed != 'True':
                self.logger.info('|    \t* Success - already in db.')
                data = json.loads(prev_failed)
                return data

            if not RETRY_FAILED_URLS:
                self.logger.info('|    \t* Failure - already in db.')
                return

        soup = make_soup(target_url)
        tags = soup.find_all('script', {'type': 'application/ld+json'})
        if len(tags) != 1:
            self.logger.info('|    \t* Failure - bad html')
            RedisManager.save(target_url, True)  # set as prev failed.
            return

        try:
            # reason for 'strict' in stack overflow's 9295439.
            obj = json.loads(tags[0].string, strict=False)
        except json.JSONDecodeError:
            self.logger.info('|    \t* Failure - bad json in html')
            RedisManager.save(target_url, True)
            return

        try:
            ac = {  # article content
                'source': {'id': self.id_, 'name': self.name},
                'author': unescape(obj['author']),
                'headline': unescape(obj['alternativeHeadline']),
                'summary': unescape(obj['description']),
                'body': unescape(obj['articleBody']).replace('&nbsp;', ' '),
                'section': section,
                'urlToImage': unescape(obj['image']['Url']),
                'url': target_url,
                'publishedAt': unescape(obj['datePublished']),
            }

            if len(ac['body']) > 5000:
                self.logger.info('|    \t* Failure - json is too big in html')
                RedisManager.save(target_url, True)
                return

            RedisManager.save(target_url, json.dumps(ac).encode())
            self.logger.info('|    \t* Success - saved to db.')
            return ac
        except KeyError:
            self.logger.info('|    \t* Failure - bad json key in html\n%s', traceback.format_exc())
            RedisManager.save(target_url, True)
            return
        except Exception:
            self.logger.critical(traceback.format_exc())
            RedisManager.save(target_url, True)
            return

    def _get_section_generator(self, url, section):
        self.logger.info('Scrapping %s', section)

        soup = make_soup(url)
        tags = soup.find_all('div', {'class': 'story'})
        if len(tags) != 1:
            self.logger.info('Error: bad html [%s]', url)
            return

        tags = tags[0].find_all('div', {'class': 'col-primary'})
        if len(tags) != 1:
            self.logger.info('Error: bad html [%s]', url)
            return

        a_list = tags[0].find_all('article')
        for a in a_list:
            try:
                a_loc = a.figure.a.get('href')
                a_obj = self._scrap_article(a_loc, section)
                yield a_obj
            except Exception:
                self.logger.error('Error scrapping [%s]\n%s', url, traceback.format_exc())
                continue

    def _scrap_section(self, section, date):
        url = '%s/archivo/%s/%s/' % (self.BASE_URL, section, date)
        generator = self._get_section_generator(url, section)
        data = []
        if generator is not None:
            # ac (article content) refers to the scrapped article's data.
            for ac in generator:
                if ac is not None:
                    data.append(ac)
        return data

    def run(self, section=None, date=None):
        """
        Scrap a section with given date.
        If a section is not provided, use all possible sections.
        If a date is not provided, use today's date in peruvian time.
        """
        if date is not None:
            if not re.match('\d{4}-\d{2}-\d{2}', str(date)):
                raise TypeError(date, '%s is not a valid date.' % date)
            target_date = date
        else:  # Use current peruvian date by default.
            target_date = datetime.datetime.now(pytz.timezone('America/Lima'))
            target_date = target_date.strftime('%Y-%m-%d')

        # Scrap all sections if None is specified.
        sections = [section] if section is not None else self.SECTIONS

        for section in sections:
            data = self._scrap_section(section, target_date)
            if data:
                try:
                    self.webserver.send_payload({
                        'data': data,
                        'section': section,
                        'date': target_date,
                        'source': self.id_,
                    })
                    self.logger.info('Posted to web server.')
                except WebServerError as e:
                    self.logger.critical('Error: scrapper [%s], section [%s], date [%s]: Error %s'
                                         % (self.name, section, target_date, e))
