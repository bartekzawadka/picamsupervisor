import RPi.GPIO as GPIO
import time
from logger import Logger
import urllib2


class MonitorDaemon:
    def __init__(self, args):
        self.__resolve_config_file()
        self.stdout_path = Logger.get_log_dir() + 'process.log'
        self.stderr_path = Logger.get_log_dir() + 'process.log'
        self.stdin_path = '/dev/null'
        self.pidfile_path = '/var/run/picamsupervisor.pid'
        self.pidfile_timeout = 5

        self.alarm_sign_pin = 15
        self.logger = Logger.get_logger()

    def __read_config_file(self):
        try:
            conf = {}
            execfile("/etc/picamsupervisor/monitor.conf", conf)
            return conf
        except Exception, e:
            self.logger.error("MonitorDaemon: Error reading config file!\n%s" % e)

    def __resolve_config_file(self):
        conf = self.__read_config_file()
        if conf is not None:
            self.alarm_sign_pin = conf["alarm_sign_pin"]
            self.monitor_sleep_time = conf["monitor_sleep_time"]
        else:
            self.logger.error("MonitorDaemon: Using default values (Alarm PIN: 15, Sleep time: 1s)")
            self.alarm_sign_pin = 15
            self.monitor_sleep_time = 1


    def __get_broadcast_destination_hosts(self):
        conf = self.__read_config_file()
        if conf is not None:
            return conf["recorders_address_list"]

    def __broadcast_alarm_info(self):
        conf = self.__read_config_file()
        if conf is not None and conf["recorders_address_list"] is not None:
            for host in conf["recorders_address_list"]:
                try:
                    result = urllib2.urlopen("http://"+host+"/start_recording").read()
                    if result == 1:
                        self.logger.info("MonitorDaemon: Record start signal successfully sent to host %s" % host)
                    else:
                        self.logger.warning("MonitorDaemon: Unable to start recording on host %s" % host)
                except Exception, e:
                    self.logger.error("MonitorDaemon: Error occurred sending start signal to host %s\n%s" % (host, e))

    def start(self):
        self.logger.info("MonitorDaemon: PiCamSupervisor monitor daemon - listener startup")

    def stop(self):
        self.logger.info("MonitorDaemon: PiCamSupervisor monitor daemon - listener stop")

    def restart(self):
        self.logger.info("MonitorDaemon: PiCamSupervisor monitor daemon - listener restart")

    def run(self):
        self.logger.info("MonitorDaemon: Initializing GPIO")

        try:
            GPIO.setwarnings(False)
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(self.alarm_sign_pin, GPIO.IN)
            self.logger.info("MonitorDaemon: GPIO initialized")
        except Exception, e:
            self.logger.fatal("MonitorDaemon: GPIO initialization failed! Monitor cannot listen!\n%s" % e)
        else:
            while True:
                if not GPIO.input(self.alarm_sign_pin):
                    time.sleep(self.monitor_sleep_time)
                if not GPIO.input(self.alarm_sign_pin):
                    self.logger.warning(
                        "MonitorDaemon: ALARM SIGNAL DETECTED! Broadcasting record message to recorders")
                    self.__broadcast_alarm_info()
                time.sleep(self.monitor_sleep_time)
