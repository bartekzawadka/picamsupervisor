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
