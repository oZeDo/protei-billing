import logging


class Logger(object):
    def __init__(self, name, log_level=None):
        if not log_level:
            log_level = 'DEBUG'

        logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')
        self.level = logging.getLevelName(log_level)
        self.logger = logging.getLogger(name)
        self.logger.setLevel(self.level)

    def get(self):
        return self.logger
