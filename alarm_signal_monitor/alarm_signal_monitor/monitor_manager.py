import time
import urllib2
import RPi.GPIO as GPIO
from picamsupervisor_logger import Logger


class MonitorManager:
    def __init__(self):

        self.logger = Logger.get_logger("Alarm-Signal-Monitor")
        self.__resolve_config_file()

    def __read_config_file(self):
        try:
            conf = {}
            execfile("/etc/picamsupervisor/monitor.conf", conf)
            return conf
        except Exception, e:
            self.logger.error("MonitorManager: Error reading config file!\n%s" % e)

    def __resolve_config_file(self):
        conf = self.__read_config_file()
        if conf is not None:
            self.alarm_sign_pin = conf["alarm_sign_pin"]
            self.monitor_sleep_time = conf["monitor_sleep_time"]
        else:
            self.logger.error("MonitorManager: Using default values (Alarm PIN: 15, Sleep time: 1s)")
            self.alarm_sign_pin = 15
            self.monitor_sleep_time = 1

    def __get_broadcast_destination_hosts(self):
        conf = self.__read_config_file()
        if conf is not None:
            hosts = None
            port = None
            try:
                hosts = conf["recorders_address_list"]
            except Exception, e:
                self.logger.warning("MonitorManager: Error reading hosts addresses. Property could not be found or is invalid")
                return hosts
            try:
                port = conf["recorder_service_port"]
            except Exception, e:
                self.logger.warning("MonitorManager: Error reading hosts communication port!. Property could not be found or is invalid")
                return None

            if hosts is None or len(hosts) == 0:
                return None

            newhosts = []
            for host in hosts:
                p = "%s" % port
                newhosts.append(host + ":" + p)
            return newhosts

    def __broadcast_alarm_info(self):
        hosts = self.__get_broadcast_destination_hosts()
        if hosts is None:
            self.logger.warning("MonitorManager: Alarm signal info was not broadcasted. No recorders found.")
            return

        for host in hosts:
            try:
                result = urllib2.urlopen("http://" + host + "/start_recording").read()
                self.logger.info("MonitorManager: RESPONSE: %s" % result)
                if result == "1":
                    self.logger.info("MonitorManager: Record start signal successfully sent to host %s" % host)
                else:
                    self.logger.warning("MonitorManager: Unable to start recording on host %s" % host)
            except Exception, e:
                self.logger.error("MonitorManager: Error occurred sending start signal to host %s\n%s" % (host, e))

    def start(self):
        self.logger.info("MonitorManager: Listener startup")
        self.__run()

    def stop(self):
        self.logger.info("MonitorManager: Listener stop")

    def restart(self):
        self.logger.info("MonitorManager: Listener restart")

    def __run(self):
        self.logger.info("MonitorManager: Initializing GPIO")

        try:
            GPIO.setwarnings(False)
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(self.alarm_sign_pin, GPIO.IN)
            self.logger.info("MonitorManager: GPIO initialized")
        except Exception, e:
            self.logger.error("MonitorManager: GPIO initialization failed! Monitor cannot listen!\n%s" % e)
        else:
            while True:
                if not GPIO.input(self.alarm_sign_pin):
                    time.sleep(self.monitor_sleep_time)
                if not GPIO.input(self.alarm_sign_pin):
                    self.logger.warning("MonitorManager: ALARM SIGNAL DETECTED! Broadcasting record message to recorders")
                    self.__broadcast_alarm_info()
                time.sleep(self.monitor_sleep_time)