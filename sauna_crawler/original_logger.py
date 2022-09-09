import logging
from logging import getLogger, config
from os.path import expanduser

class OriginalLogger:
    
    LOG_FILE_PATH = '{}/log/sauna-crawler/application.log'.format(expanduser("~"))
    
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
            
            # ログファイルの設定
            fh = logging.FileHandler(self.LOG_FILE_PATH)
            fh.setLevel(logging.INFO)
            fh.setFormatter(ch_formatter)
            self.logger.addHandler(fh)
    
    def debug(self, message):
        self.logger.debug(message)
         
    def info(self, message):
        self.logger.info(message)
    
    def warn(self, message):
        self.logger.warn(message)
        
    def error(self, message):
        self.logger.error(message)