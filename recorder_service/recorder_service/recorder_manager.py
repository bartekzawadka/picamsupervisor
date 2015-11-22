import os
from logger import Logger
import RPi.GPIO as GPIO
from recorder_runner import RecorderRunner


class RecorderManager:
    def __init__(self):
        self.logger = Logger.get_logger("Recorder-Service")
        self.__set_parameters()
        self.__initialize_gpio()
        self.record_task = RecorderRunner(group=None, target=None, name="None", args=(self.record_width, self.record_height, self.record_path, self.record_time, self.record_task_finished_callback))
        self.logger.info("RecorderManager: Width: %s, Height: %s" % (self.record_width, self.record_height))

    def __set_parameters(self):
        try:
            conf = {}
            execfile("/etc/picamsupervisor/recorder.conf", conf)
            self.ir_lighting_pin = conf["ir_lighting_pin"]
            self.record_width = conf["record_width"]
            self.record_height = conf["record_height"]
            self.record_path = conf["record_path"]
            self.record_time = conf["record_time"]
        except Exception, e:
            self.logger.warning(
                "Recorder: Error reading config file. Using default values (IR lighting PIN: 16, Width: 1920, Height: 1080, Record path: /mnt/records, Record time: 40 min)")
            self.ir_lighting_pin = 16
            self.record_width = 1920
            self.record_height = 1080
            self.record_path = "/mnt/records/"
            self.record_time = 40

    def __initialize_gpio(self):
        try:
            self.logger.info("Recorder: Initializing GPIO (PIN: %s)" % self.ir_lighting_pin)
            GPIO.setwarnings(False)
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(self.ir_lighting_pin, GPIO.OUT)
            if not self.is_raspivid_running():
                GPIO.output(self.ir_lighting_pin, GPIO.HIGH)
            self.logger.info("Recorder: GPIO initialized successfully")
        except Exception, e:
            self.logger.error(
                "Recorder: GPIO INITIALIZATION FAILED!!! IR LIGHTING CONTROL MAY BE UNAVAILABLE\n%s" % e)

    def is_raspivid_running(self):
        camProcess = os.system("ps aux | grep raspivid | grep -v grep")
        self.logger.info("RecorderManager: RASPIVID CHECK RESULT: %s" % camProcess)
        if camProcess != 0:
            return False
        else:
            return True

    def __switch_ir_lighting(self, on_off):
        if on_off:
            state_text = "ON"
            gpio_state = GPIO.LOW
        else:
            state_text = "OFF"
            gpio_state = GPIO.HIGH

        self.logger.info("Recorder: Turning IR lighting %s (PIN: %s)" % (state_text, self.ir_lighting_pin))
        GPIO.output(self.ir_lighting_pin, gpio_state)
        self.logger.info("Recorder: IR lighting turned %s successfully" % state_text)

    def start_recording(self):
        self.logger.info("Recorder: Video recording start request occurred")
        try:
            self.__switch_ir_lighting(True)
            if self.is_raspivid_running(): #or (self.record_task is not None and self.record_task.is_alive):
                self.logger.info("Recorder: raspivid is already working. Nothing to be done")
            else:
                self.record_task.run()
                self.logger.info("Recorder: raspivid task executed. Recording started")

            return True
        except Exception, e:
            self.logger.error("Recorder: Error executing raspivid!\n%s" % e)
            return False

    def stop_recording(self):
        self.logger.info("Recorder: Video recording kill request occurred")

        try:
            if self.is_raspivid_running():
                code = os.system("killall -9 raspivid")
                self.logger.info("Recorder: Video kill finished. Exit code: %s" % code)
            else:
                self.logger.info("Recorder: No raspivid process to be killed")

            self.__switch_ir_lighting(False)
            return True
        except Exception, e:
            self.logger.error("Recorder: Killing video recording failed!\n%s" % e)
            return False

    def record_task_finished_callback(self, result):
        self.__switch_ir_lighting(False)
        self.logger.info("Recorder: raspivid process finished")
