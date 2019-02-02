import sys
import time

from scrappy import settings
from scrappy.logger import Logger
from scrappy.scrappers import engines


class App:

    def __init__(self):
        self.logger = Logger()

        # sleep for this much time before running
        # scrapper again.
        self.T = 60 * 5

    def run_dev(self):
        for engine in engines:
            engine(self.logger).run(section='politica')

    def run_prod(self):
        for engine in engines:
            engine(self.logger).run()

    def run(self):
        try:
            while True:
                if not settings.PRODUCTION:
                    self.run_dev()
                else:
                    self.run_prod()
                # hogging the cpu but should not be
                # a big deal. Look into this if it
                # ever becomes a problem.
                time.sleep(self.T)
        except RuntimeError as e:
            raise
        except KeyboardInterrupt:
            self.logger.info('Shutting down')
            sys.exit()


def run():
    App().run()


if __name__ == '__main__':
    run()
