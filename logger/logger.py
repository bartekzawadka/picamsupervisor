import logging
import logging.handlers


class Logger:

    __logger = None
    __logdir = None
    __logpath = __logdir + "picamsupervisor.log"

    def __resolve_config_file(self):
        if Logger.__logdir is None:
            conf = {}
            try:
                execfile("/etc/picamsupervisor/monitor.conf", conf)
            except Exception, e:
                Logger.__logdir = "/var/log/picamsupervisor/"
                Logger.get_logger().error("Logger: Could not resolve config file! Default log files path used")
            else:
                Logger.__logdir = conf["logs_path"]

    def get_log_dir(self):
        if Logger.__logdir is None:
            Logger.__resolve_config_file()
        return Logger.__logdir

    def get_logger(self):
        if Logger.__logdir is None:
            Logger.__resolve_config_file()
        if Logger.__logger is None:
            logger = logging.getLogger("PiCamSupervisorLog")
            formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
            thandler = logging.handlers.TimedRotatingFileHandler(Logger.__logpath, when="midnight")
            thandler.suffix = "%Y-%m-%d"
            thandler.setFormatter(formatter)
            logger.addHandler(thandler)
            Logger.__logger = logger
        return Logger.__logger
