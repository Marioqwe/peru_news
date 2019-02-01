import datetime
import pytz
import re

from scrappy._http import WebServer
from scrappy.exceptions import WebServerError


class Scrapper(object):

    id_ = None
    name = None

    BASE_URL = None
    SECTIONS = []

    def __init__(self, logger):
        self.logger = logger
        self.webserver = WebServer()

    def _scrap_section(self, section, date):
        raise NotImplementedError

    def run(self, section=None, date=None, test=False):
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
                if test:
                    return
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
