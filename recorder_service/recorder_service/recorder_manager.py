import os
from logger import Logger
import RPi.GPIO as GPIO
from recorder_runner import RecorderRunner


class RecorderManager:
    def __init__(self):
        self.__set_parameters()
        self.__initialize_gpio()
        self.record_task = RecorderRunner(self.record_width, self.record_height, self.record_path, self.record_time,
                                          self.record_task_finished_callback)

    def __set_parameters(self):
        try:
            conf = {}
            execfile("/etc/picamsupervisor/recorder.config", conf)
            self.ir_lighting_pin = conf["ir_lighting_pin"]
            self.record_width = conf["record_width"]
            self.record_height = conf["record_height"]
            self.record_path = conf["record_path"]
            self.record_time = conf["record_time"]
        except Exception, e:
            Logger.get_logger().warn(
                "Recorder: Error reading config file. Using default values (IR lighting PIN: 16, Width: 1920, Height: 1080, Record path: /mnt/records, Record time: 40 min)")
            self.ir_lighting_pin = 16
            self.record_width = 1920
            self.record_height = 1080
            self.record_path = "/mnt/records/"
            self.record_time = 40

    def __initialize_gpio(self):
        try:
            Logger.get_logger().info("Recorder: Initializing GPIO (PIN: %s)" % self.ir_lighting_pin)
            GPIO.setwarnings(False)
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(self.ir_lighting_pin, GPIO.OUT)
            if not self.is_raspivid_running():
                GPIO.output(self.ir_lighting_pin, GPIO.HIGH)
            Logger.get_logger().infor("Recorder: GPIO initialized successfully")
        except Exception, e:
            Logger.get_logger().fatal(
                "Recorder: GPIO INITIALIZATION FAILED!!! IR LIGHTING CONTROL MAY BE UNAVAILABLE\n%s" % e)

    def is_raspivid_running(self):
        camProcess = os.system("ps aux | grep raspivid | grep -v grep")
        if camProcess == 0:
            return True
        else:
            return False

    def __switch_ir_lighting(self, on_off):
        if on_off:
            state_text = "ON"
            gpio_state = GPIO.LOW
        else:
            state_text = "OFF"
            gpio_state = GPIO.HIGH

        Logger.get_logger().info("Recorder: Turning IR lighting %s (PIN: %s)" % (state_text, self.ir_lighting_pin))
        GPIO.output(self.ir_lighting_pin, gpio_state)
        Logger.get_logger().info("Recorder: IR lighting turned %s successfully" % state_text)

    def start_recording(self):
        Logger.get_logger().info("Recorder: Video recording start request occurred")
        try:
            self.__switch_ir_lighting(True)
            if self.is_raspivid_running() or (self.record_task is not None and self.record_task.is_alive):
                Logger.get_logger().info("Recorder: raspivid is already working. Nothing to be done")
            else:
                self.record_task.run()
                Logger.get_logger().info("Recorder: raspivid task executed. Recording started")

            return True
        except Exception, e:
            Logger.get_logger().fatal("Recorder: Error executing raspivid!\n" % e)
            return False

    def stop_recording(self):
        Logger.get_logger().info("Recorder: Video recording kill request occurred")

        try:
            if self.is_raspivid_running():
                code = os.system("killall -9 raspivid")
                Logger.get_logger().info("Recorder: Video kill finished. Exit code: %s" % code)
            else:
                Logger.get_logger().info("Recorder: No raspivid process to be killed")

            self.__switch_ir_lighting(False)
            return True
        except Exception, e:
            Logger.get_logger().error("Recorder: Killing video recording failed!\n%s" % e)
            return False

    def record_task_finished_callback(self, result):
        self.__switch_ir_lighting(False)
        Logger.get_logger().info("Recorder: raspivid process finished")
