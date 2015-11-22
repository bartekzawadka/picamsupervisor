import flask
from recorder_manager import RecorderManager
from logger import Logger

app = flask.Flask(__name__)
rec = RecorderManager()


@app.route('/start_recording')
def start_recording():
    return "%d" % rec.start_recording()


@app.route('/stop_recording')
def stop_recording():
    return "%d" % rec.stop_recording()


if __name__ == '__main__':
    try:
        conf = {}
        execfile("/etc/picamsupervisor/recorder.conf", conf)
        port = conf["recorder_service_port"]
    except Exception, e:
        Logger.get_logger("Recorder-Service").warning(
            "RecorderService: Service initialization - cannot read config file. Using default port (808)")
        port = 808

    app.run(host='0.0.0.0', port=port, debug=True)
