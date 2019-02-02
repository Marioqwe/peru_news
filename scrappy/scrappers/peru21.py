from datetime import datetime

from scrappy.logger import Logger
from scrappy.scrappers.base import Scrapper
from scrappy.utils import make_soup


class Peru21(Scrapper):

    id_ = 'peru21'
    name = 'Peru 21'

    BASE_URL = 'https://peru21.pe'
    SECTIONS = ('politica', 'mundo', 'economia',
                'deportes', 'tecnologia',)

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
                timestamp = time.get('datetime')
                date = datetime.fromtimestamp(float(timestamp))

                data.append({
                    'source': {'id': self.id_, 'name': self.name},
                    'headline': title,
                    'section': section,
                    'url': url,
                    'publishedAt': str(date),
                })

        self.logger.info('Found [%s] articles', len(data))
        return data


if __name__ == '__main__':
    logger = Logger()
    scrapper = Peru21(logger)
    scrapper.run(section='politica', test=True)
