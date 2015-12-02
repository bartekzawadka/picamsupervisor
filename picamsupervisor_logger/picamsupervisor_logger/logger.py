import logging
import logging.handlers
import logging.config


class Logger:

    __handler = None

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
            thandler = logging.handlers.TimedRotatingFileHandler(Logger.get_logs_dir() + 'picamsupervisor.log', when="midnight")
            thandler.suffix = "%Y-%m-%d"
            thandler.setFormatter(formatter)
            Logger.__handler = thandler
        return Logger.__handler

    @staticmethod
    def get_logs_dir():
        try:
            conf = {}
            execfile("/etc/picamsupervisor/log.conf", conf)
            path = conf["log_dir"]
        except Exception, e:
            path = '/var/log/picamsupervisor/'
        return path
