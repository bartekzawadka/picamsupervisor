import flask
import sys

from picamsupervisor_logger import Logger
from recorder_manager import RecorderManager

app = flask.Flask(__name__)
rec = RecorderManager()


@app.route('/start_recording')
def start_recording():
    return "%d" % rec.start_recording()


@app.route('/stop_recording')
def stop_recording():
    return "%d" % rec.stop_recording()

def shutdown_server():
    func = flask.request.environ.get('werkzeug.server.shutdown')
    if func is None:
        Logger.get_logger("Recorder-Service").warning("Service could not be stopped - not running with the Werkzeug Server")
    func()


if __name__ == '__main__':
    try:
        conf = {}
        execfile("/etc/picamsupervisor/recorder.conf", conf)
        port = conf["recorder_service_port"]
    except Exception, e:
        Logger.get_logger("Recorder-Service").warning(
            "RecorderService: Service initialization - cannot read config file. Using default port (808)")
        port = 808

    if sys.argv[1] == "start":
        app.run(host='0.0.0.0', port=port, debug=False)
    elif sys.argv[1] == "stop":
        shutdown_server()
