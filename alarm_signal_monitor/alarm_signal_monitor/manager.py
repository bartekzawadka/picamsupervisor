import sys

from daemon import runner

from monitordaemon import MonitorDaemon
from picamsupervisor_logger import Logger


def main(args):
    if len(args) != 2:
        print "Invalid number of arguments. Only 1 argument expected"
    else:
        monitord = MonitorDaemon(args)

        if args[1] == "start":
            monitord.start()
        elif args[1] == "stop":
            monitord.stop()
        elif args[1] == "restart":
            monitord.restart()

        drunner = runner.DaemonRunner(monitord)
        drunner.daemon_context.files_preserve = [Logger.get_handler().stream]
        drunner.do_action()


if __name__ == '__main__':
    sys.exit(main(sys.argv))
