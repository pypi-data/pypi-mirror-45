import logging
import time
from os.path import join
import os


class _EasyLogging:
    def __init__(self, function, config={}):
        self.function = function
        self.file_name = config.get("FILE_NAME", "time.log")
        self.app_code = config.get("APP_CODE", "default")
        self.logger=self.initialize_logger()

    def __call__(self, *args, **kwargs):

        start_time = time.time()
        try:
            self.function(*args, **kwargs)
        except Exception as e:
            raise e
        end_time = time.time()
        extras = {'exec_time': end_time-start_time,
                  'app_code': self.app_code, 'function_name': self.function.__name__}
        self.logger.info(None, extra=extras)
    def initialize_logger(self):
        logger = logging.getLogger("execution_time_log")
        self.generate_log_if_not_exist()
        if not logger.hasHandlers():
            logger.setLevel(logging.INFO)
            filehandler = logging.FileHandler(self.file_name)
            formatter = logging.Formatter(
                '%(asctime)s - %(app_code)s - %(function_name)s - %(exec_time)f')
            filehandler.setFormatter(formatter)
            logger.addHandler(filehandler)
        return logger
    def generate_log_if_not_exist(self):
        splited_array=self.file_name.split(os.sep)
        if len(splited_array)>1:
            dir_location=os.sep.join(splited_array[:-1])
            if not os.path.exists(dir_location):
                os.makedirs(dir_location)

def log(function=None, config=None):
    if function:
        return _EasyLogging(function)
    else:
        def wrapper(function):
            return _EasyLogging(function, config)
        return wrapper

