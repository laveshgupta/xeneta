import logging
from constants import Constants
import traceback

class Logger:
    __instance = None

    @staticmethod
    def get_instance():
        """
        Singleton function for logger class 
        """
        if Logger.__instance == None:
            Logger()
        return Logger.__instance


    def __init__(self):
        if Logger.__instance != None:
            raise Exception("This class is a Singleton!")
        else:
            self.__create_logger()
            Logger.__instance = self


    def __create_logger(self):
        """
        Create logger having both stream and file handler
        """
        logging_config = config.get('logging', {})
        log_level = logging_config.get('level', Constants.LOG_LEVEL)
        log_file = logging_config.get('log_file', Constants.LOG_FILE)
        logger = logging.getLogger()
        logger.setLevel(Constants.LOGGING_LEVELS[log_level])
        log_format = logging.Formatter(fmt='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
        ch = logging.StreamHandler()
        ch.setFormatter(log_format)
        logger.addHandler(ch)
        try:
            fh = logging.FileHandler(log_file)
        except Exception as e:
            print("ERROR: Could not open/create log file {0}. Error: {1}".format(log_file, traceback.print_exc(e)))
            exit(1)
        fh.setFormatter(log_format)
        logger.addHandler(fh)
        self.__logger = logger


    def info(self, message):
        self.log('INFO', message=message)


    def debug(self, message):
        self.log('DEBUG', message=message)


    def warning(self, message):
        self.log('WARNING', message=message)


    def error(self, message):
        self.log('ERROR', message=message)


    def critical(self, message):
        self.log('CRITICAL', message=message)


    def exception(self, message):
        self.log('EXCEPTION', message=message)


    def log(self, severity:str, message:str):
        if severity == 'DEBUG':
            self.__logger.debug(message)
        elif severity == 'INFO':
            self.__logger.info(message)
        elif severity == 'WARNING':
            self.__logger.warn(message)
        elif severity == 'ERROR':
            self.__logger.error(message)
        elif severity == 'CRITICAL':
            self.__logger.critical(message)
        elif severity == 'EXCEPTION':
            self.__logger.exception(message)
