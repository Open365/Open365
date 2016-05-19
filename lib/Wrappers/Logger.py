import logging
import os
from lib.Settings import Settings
from lib.Wrappers.NullLogger import NullLogger


class Logger:
    def __init__(self, name):
        if 'UNITTESTING' in os.environ:
            self.logging = NullLogger()
        else:
            settings = Settings().getSettings()
            logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                                level=settings["logs"]["level"])
            self.logging = logging.getLogger(name)

    def debug(self, *args, **kwargs):
        self.logging.debug(*args, **kwargs)

    def info(self, *args, **kwargs):
        self.logging.info(*args, **kwargs)

    def warning(self, *args, **kwargs):
        self.logging.warning(*args, **kwargs)

    def error(self, *args, **kwargs):
        self.logging.error(*args, **kwargs)

    def critical(self, *args, **kwargs):
        self.logging.critical(*args, **kwargs)

    def log(self, *args, **kwargs):
        self.logging.log(*args, **kwargs)
