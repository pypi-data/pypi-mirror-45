#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import threading
import time
from pprint import pprint
import traceback
import json


DYNLOGS = ['']

LOGS_LEVEL = os.environ.get('XIO_LOGS_LEVEL', 'INFO').upper()
LOGS_DIR = os.environ.get('XIO_LOGS_DIR')


def getLogServiceHandler(**config):

    import sys
    import logging
    from logging.handlers import RotatingFileHandler

    def colorize(txt, code, background=False):

        if code == BOLD:
            return BOLD_SEQ + txt + RESET_SEQ
        elif code:

            TYPE = CODE_BACKGROUND if background else CODE_FOREGROUND
            return COLOR_SEQ % (TYPE + code) + txt + RESET_SEQ
        else:
            return txt

    class ColoredFormatter(logging.Formatter):

        def __init__(self, pattern):
            logging.Formatter.__init__(self, pattern)

        def format(self, record):
            mapping = {
                'WARNING': YELLOW,
                'INFO': GREEN,
                'DEBUG': WHITE,
                'CRITICAL': RED,
                'ERROR': RED
            }
            record.levelname = colorize(record.levelname, mapping.get(record.levelname))
            return logging.Formatter.format(self, record)

    class CustomAdapter(logging.LoggerAdapter):

        def process(self, msg, kwargs, **k):
            DYNLOGS.append(msg)
            if len(DYNLOGS) > 1000:
                DYNLOGS.pop(0)

            if 'path' in kwargs:
                path = kwargs.pop('path') or '/'
            else:
                path = ''
            if 'ext' in kwargs:
                ext = kwargs.pop('ext') or ''
                ext = '\t%s' % ext + ' ' * (20 - len(ext))
            else:
                ext = ''
            kwargs = {'extra': kwargs}
            kwargs['extra']['path'] = path
            kwargs['extra']['ext'] = ext
            return msg, kwargs

    RESET_SEQ = "\033[0m"
    COLOR_SEQ = "\033[1;%dm"
    BOLD_SEQ = "\033[1m"
    CODE_BACKGROUND = 40
    CODE_FOREGROUND = 30
    BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = list(range(8))
    BOLD = -1

    logger = logging.getLogger('xio')
    logger.setLevel(logging.DEBUG)

    stdoutHandler = logging.StreamHandler(sys.stdout)
    stdoutHandler.setFormatter(ColoredFormatter('%(levelname)s\t%(ext)s%(path)s\t%(message)s'))
    logger.addHandler(stdoutHandler)

    if LOGS_DIR and os.path.isdir(LOGS_DIR):
        fileHandler = RotatingFileHandler(LOGS_DIR + '/xio.logs', 'a', 10000, 1)
        fileHandler.setLevel(logging.DEBUG)
        fileHandler.setFormatter(logging.Formatter('%(asctime)s\t%(levelname)s\t%(message)s'))
        logger.addHandler(fileHandler)

    logger = CustomAdapter(logger, {'path': '', 'ext': ''})
    return logger


def _tomsg(msg):
    return ' '.join([str(m) for m in msg])


class LogService:

    _logger = False

    def show(self):
        return DYNLOGS

    def __init__(self, level=LOGS_LEVEL, **config):

        import sys
        import logging
        from logging.handlers import RotatingFileHandler

        self.level = level

        if not LogService._logger:
            LogService._logger = getLogServiceHandler(**config)

        self.handler = LogService._logger

    def setLevel(self, level):
        self.level = level

    def info(self, *msg, **kwargs):
        if self.handler:
            msg = _tomsg(msg)
            self.handler.info(msg, **kwargs)

    def warning(self, *msg, **kwargs):
        if self.handler:
            msg = _tomsg(msg)
            self.handler.warning(msg, **kwargs)

    def error(self, *msg, **kwargs):
        if self.handler:
            msg = _tomsg(msg)
            self.handler.error(msg, **kwargs)

    def debug(self, *msg, **kwargs):
        if self.handler and self.level == 'DEBUG':
            msg = _tomsg(msg)
            self.handler.debug(msg, **kwargs)

log = LogService()
