import logging


class Logger:

    LOG_LEVELS = {
        'critical': logging.CRITICAL,
        'error': logging.ERROR,
        'warning': logging.WARNING,
        'info': logging.INFO,
        'debug': logging.DEBUG
    }

    error_fmt = r'%(asctime)s [%(process)d] [%(levelname)s] %(message)s'
    datefmt = r'[%Y-%m-%d %H:%M:%S %z]'

    def __init__(self):
        self.error_log = logging.getLogger('scrapper.error')
        self.error_log.propagate = False
        self.error_handlers = []
        self.setup()

    def setup(self):
        self.loglevel = self.LOG_LEVELS.get('info')
        self.error_log.setLevel(self.loglevel)

        # output everything to stderr
        h = logging.StreamHandler()
        h.setFormatter(logging.Formatter(self.error_fmt, self.datefmt))
        self.error_log.addHandler(h)

    def critical(self, msg, *args, **kwargs):
        self.error_log.critical(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self.error_log.error(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self.error_log.warning(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self.error_log.info(msg, *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        self.error_log.debug(msg, *args, **kwargs)

    def exception(self, msg, *args, **kwargs):
        self.error_log.exception(msg, *args, **kwargs)

    def log(self, lvl, msg, *args, **kwargs):
        if isinstance(lvl, str):
            lvl = self.LOG_LEVELS.get(lvl.lower(), logging.INFO)
        self.error_log.log(lvl, msg, *args, **kwargs)
