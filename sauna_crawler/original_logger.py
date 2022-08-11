import logging
from logging import getLogger, config

class OriginalLogger:
    def __init__(self):        
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        
        # handlerが既に存在する場合はセットしない
        if not self.logger.hasHandlers():
            # create console handler with a INFO log level
            ch = logging.StreamHandler()
            ch.setLevel(logging.INFO)
            ch_formatter = logging.Formatter('%(asctime)s [%(levelname)s] - %(message)s', '%Y-%m-%d %H:%M:%S')
            ch.setFormatter(ch_formatter)
            self.logger.addHandler(ch)
    
    def debug(self, message):
        self.logger.debug(message)
         
    def info(self, message):
        self.logger.info(message)
    
    def warn(self, message):
        self.logger.warn(message)
        
    def error(self, message):
        self.logger.error(message)