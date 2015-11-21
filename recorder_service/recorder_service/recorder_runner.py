from threading import Thread
from logger import Logger
import os
import time


class RecorderRunner(Thread):
    def __int__(self, record_width, record_height, record_destination_path, record_time, record_finished_callback):
        Thread.__init__(self)
        self.width = record_width
        self.height = record_height
        self.path = record_destination_path
        self.time = record_time
        self.record_finished_callback = record_finished_callback

    def run(self):
        global result
        try:
            Logger.get_logger().info("RecorderRunner: Record task started")
            duration = self.time * 60000
            file = self.path + time.strftime("%Y.%m.%d-%Hh.%Mm.%Ss", time.localtime()) + ".h264"
            exit_code = os.system("raspivid -t %s -w %s -h %s -o %s" % (duration, self.width, self.height, file))
            Logger.get_logger().info("RecorderRunner: Record task finished with exit code: %s" % exit_code)
            result = True
        except Exception, e:
            Logger.get_logger().fatal("RecordRunner: Record task failed!\n%s" % e)
            result = False
        finally:
            if self.record_finished_callback is not None:
                self.record_finished_callback(result)
