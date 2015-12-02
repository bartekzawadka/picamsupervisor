import os
import time
from threading import Thread

from picamsupervisor_logger import Logger


class RecorderRunner(Thread):
    def __init__(self, rec_width, rec_height, rec_dest_path, rec_time, rec_callback):
        Thread.__init__(self)
        self.logger = Logger.get_logger("Recorder-Service")
        self.width = rec_width
        self.height = rec_height
        self.path = rec_dest_path
        self.time = rec_time
        self.callback = rec_callback
        self.logger.info("RecorderRunner: Initialized")

    def run(self):
        global result
        try:
            self.logger.info("RecorderRunner: Record task started")
            duration = self.time * 60000
            file = self.path + time.strftime("%Y.%m.%d-%Hh.%Mm.%Ss", time.localtime()) + ".h264"
            exit_code = os.system("raspivid -t %s -w %s -h %s -o %s" % (duration, self.width, self.height, file))
            self.logger.info("RecorderRunner: Record task finished with exit code: %s" % exit_code)
            result = True
        except Exception, e:
            self.logger.error("RecordRunner: Record task failed!\n%s" % e)
            result = False
        finally:
            if self.callback is not None:
                self.callback(result)
