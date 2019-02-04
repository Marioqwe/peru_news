from datetime import datetime

from scrappy.logger import Logger
from scrappy.scrappers.base import Scrapper
from scrappy.settings import TIMEZONE
from scrappy.utils import make_soup


class ElComercio(Scrapper):

    id_ = 'el_comercio'
    name = 'El Comercio'

    BASE_URL = 'https://elcomercio.pe'
    SECTIONS = ('politica', 'mundo', 'economia', 'tecnologia',)

    def _scrap_section(self, section, date):
        url = '%s/archivo/%s/%s/' % (self.BASE_URL, section, date)
        self.logger.info('%s', url)
        soup = make_soup(url)
        res_set = soup.find_all('div', {'class': 'column-flows'})
        if len(res_set) != 1:
            return
        res = res_set[0]
        articles = res.find_all('article')
        data = []
        for article in articles:
            h2 = article.h2
            time = article.time
            if h2 and time:
                title = h2.a.get_text()
                url = self.BASE_URL + h2.a.get('href')
                aid = url.split('-')[-1]
                timestamp = time.get('datetime')
                date = datetime.fromtimestamp(float(timestamp), tz=TIMEZONE)
                iso_date = date.isoformat()
                data.append({
                    'aid': aid,
                    'headline': title,
                    'section': section,
                    'url': url,
                    'publishedAt': iso_date,
                })

        self.logger.info('Found [%s] articles', len(data))
        return data


if __name__ == '__main__':
    logger = Logger()
    scrapper = ElComercio(logger)
    scrapper.run(section='politica', test=True)
