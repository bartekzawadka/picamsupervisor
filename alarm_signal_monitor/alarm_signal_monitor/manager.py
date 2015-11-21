import sys
from monitordaemon import MonitorDaemon
from daemon import runner


def main(args):
    if len(args) != 2:
        print "Invalid number of arguments. Only 1 argument expected"
    else:
        monitord = MonitorDaemon()

        if args[1] == "start":
            monitord.start()
        elif args[1] == "stop":
            monitord.stop()
        elif args[1] == "restart":
            monitord.restart()

        runner.DaemonRunner(monitord).do_action()


if __name__ == '__main__':
    sys.exit(main(sys.argv))
