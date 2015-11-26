from threading import Thread
from logger import Logger
import os
import time


class RecorderRunner(Thread):
    def __int__(self):
        Thread.__init__(self)
        self.logger = Logger.get_logger("Recorder-Service")
        #self.width = recorder_manager.record_width
        #self.height = recorder_manager.record_height
        #self.path = recorder_manager.record_destination_path
        #self.time = recorder_manager.record_time
        self.logger.info("RecorderRunner: Initialized")

    def run(self):
        global result
        try:
            self.logger.info("RecorderRunner: Record task started")
            #duration = self.time * 60000
            #file = self.path + time.strftime("%Y.%m.%d-%Hh.%Mm.%Ss", time.localtime()) + ".h264"
            #exit_code = os.system("raspivid -t %s -w %s -h %s -o %s" % (duration, self.width, self.height, file))
            exit_code = 0
            self.logger.info("RecorderRunner: RECORDING BLA BLA BLA")
            self.logger.info("RecorderRunner: Record task finished with exit code: %s" % exit_code)
            result = True
        except Exception, e:
            self.logger.error("RecordRunner: Record task failed!\n%s" % e)
            result = False
        # finally:
        #     if self.recorder_manager is not None:
        #         self.recorder_manager(result)
