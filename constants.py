import logging

class Constants:
    APP_CONFIG_FILE_PATH = 'ratestask_config.json'
    DEFAULT_DB_MIN_CONN = 1
    DEFAULT_DB_MAX_CONN = 1
    DEFAULT_DB_HOST = 'localhost'
    DEFAULT_DB_PORT = 5432
    DEFAULT_DB_DATABASE = 'postgres'
    DEFAULT_DB_USER = 'postgres'
    DEFAULT_DB_PASSWORD = 'ratestask'
    LOG_LEVEL = 'DEBUG'
    LOGGING_LEVELS = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }
    LOG_FILE = 'ratestask.log'
    APP_HOST = '0.0.0.0'
    APP_PORT = 80
    PORT_REGION_CODE = {
        'none': 0,
        'port': 1,
        'region': 2
    }
    INTEGRATION_TESTS_CASES_FILE = 'ratestask_integration_tests.json'
