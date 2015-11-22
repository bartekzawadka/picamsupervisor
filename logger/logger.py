import logging
import logging.handlers
import logging.config


class Logger:

    __handler = None
    __logdir = "/var/log/picamsupervisor/"

    @staticmethod
    def get_logger(modulename):
        logger = logging.getLogger(name="PiCamSupervisor."+modulename)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(Logger.get_handler())
        return logger

    @staticmethod
    def get_handler():
        if Logger.__handler is None:
            formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
            thandler = logging.handlers.TimedRotatingFileHandler(Logger.__logdir + 'picamsupervisor.log', when="midnight")
            thandler.suffix = "%Y-%m-%d"
            thandler.setFormatter(formatter)
            Logger.__handler = thandler
        return Logger.__handler

    @staticmethod
    def get_logs_dir():
        return Logger.__logdir


# class Logger:
#     def __init__(self):
#         self.__logdir = "/var/log/picamsupervisor/"
#         self.__logpath = self.__logdir + "picamsupervisor.log"
#
#         self.__logger = logging.getLogger("PiCamSupervisorLog")
#         self.__logger.setLevel(logging.DEBUG)
#         formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
#         self.__thandler = logging.handlers.TimedRotatingFileHandler(self.__logpath, when="midnight")
#         self.__thandler.suffix = "%Y-%m-%d"
#         self.__thandler.setFormatter(formatter)
#
#         self.__logger.addHandler(self.__thandler)
#
#     def get_time_rotation_file_handler(self):
#         return self.__thandler
#
#     def get_log_dir(self):
#         return self.__logdir
#
#     def get_logger(self):
#         return self.__logger
