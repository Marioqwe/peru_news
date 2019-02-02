from scrappy.logger import Logger
from scrappy.scrappers.base import Scrapper
from scrappy.utils import make_soup


class RPP(Scrapper):

    id_ = 'rpp'
    name = 'RPP Noticias'

    BASE_URL = 'http://www.rpp.pe'
    SECTIONS = ('politica', 'mundo', 'economia',
                'actualidad', 'deportes', 'entretenimiento',)

    def _scrap_section(self, section, date):
        url = '%s/archivo/%s/%s/' % (self.BASE_URL, section, date)
        self.logger.info('%s', url)
        soup = make_soup(url)
        res_set = soup.find_all('div', {'class': 'col-primary'})
        if len(res_set) != 1:
            return
        res = res_set[0]
        articles = res.find_all('article')
        data = []
        for article in articles:
            h3 = article.h3
            time = article.time
            if h3 and time:
                title = h3.a.get_text()
                url = self.BASE_URL + h3.a.get('href')
                date = time.get('data-x')

                data.append({
                    'source': {'id': self.id_, 'name': self.name},
                    'headline': title,
                    'section': section,
                    'url': url,
                    'publishedAt': date,
                })

        self.logger.info('Found [%s] articles', len(data))
        return data


if __name__ == '__main__':
    logger = Logger()
    scrapper = RPP(logger)
    scrapper.run(section='politica', test=True)
