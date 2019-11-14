import logging

import os
from logging.handlers import RotatingFileHandler


class LogLevelFilter(logging.Filter):
    def __init__(self, name='', level=logging.DEBUG):
        super(LogLevelFilter, self).__init__(name)
        self.level = level

    def filter(self, record):
        return record.levelno == self.level


class LogMgr(object):
    loggers = dict()

    @classmethod
    def get(cls, name='default', log_dir='logs'):

        if name not in cls.loggers:
            _logger = logging.getLogger(name)
            _logger.setLevel(logging.DEBUG)

            fmt = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
            levels = [logging.INFO, logging.DEBUG, logging.ERROR]
            for level in levels:
                fn = '%s/%s/%s.log' % (log_dir, logging.getLevelName(level).lower(), name)
                if '.pyc' in fn:
                    fn = fn.replace('.pyc', '')
                if not os.path.exists(os.path.dirname(fn)):
                    os.makedirs(os.path.dirname(fn))

                file_handler = RotatingFileHandler(filename=fn, maxBytes=100 * 1024 * 1024, backupCount=10, delay=1)
                file_handler.setLevel(level)
                file_handler.setFormatter(fmt)
                file_handler.addFilter(LogLevelFilter(level=level))
                _logger.addHandler(file_handler)

                console_handler = logging.StreamHandler()
                console_handler.setLevel(level)
                console_handler.setFormatter(fmt)
                console_handler.addFilter(LogLevelFilter(level=level))
                _logger.addHandler(console_handler)

                cls.loggers[name] = _logger

        return cls.loggers.get(name)
