from flask import Flask, request
from flask_cors import CORS
import json
from Cache import Cache
from Protocols import Protocols
from AlarmManager import AlarmManager


class WebServer:

    listener = None

    def __init__(self):
        # Flask instance to receive data
        self.app = Flask(__name__)
        CORS(self.app)

    @staticmethod
    def get_instance():
        if WebServer.listener is None:
            WebServer.listener = WebServer()
        return WebServer.listener

    def listen(self, ip, port):
        # execute the listening server, for each message received, it will be handled by a thread
        self.app.run(host=ip, port=port, debug=False, threaded=True)

    def get_app(self):
        return self.app


app = WebServer.get_instance().get_app()


@app.post('/status')
def post_status():
    if request.json is None:
        return {'error': 'No JSON request received'}, 500

    received_json = request.json
    print(f'[Web server] received {received_json}')
    status = Protocols.status()
    return {"status": 0, "body": json.dumps(status)}

@app.post('/remove')
def post_remove():
    if request.json is None:
        return {'error': 'No JSON request received'}, 500

    received_json = request.json
    print(f'[Web server] received {received_json}')
    status = 0
    if (received_json['type'] == 'node') and ('node_id' in received_json):
        Protocols.remove(received_json['node_id'])
    else:
        status = -1
    return {"status": status, "body": json.dumps({'cmd': 'remove'})}

@app.post('/keep_alive')
def post_keep_alive():
    if request.json is None:
        return {'error': 'No JSON request received'}, 500

    received_json = request.json
    print(f'[Web server] received {received_json}')
    Protocols.keep_alive()
    return {"status": 0, "body": json.dumps({'cmd': 'keep_alive'})}

@app.post('/alarm_on')
def post_alarm_on():
    if request.json is None:
        return {'error': 'No JSON request received'}, 500

    received_json = request.json
    print(f'[Web server] received {received_json}')
    status = 0
    if received_json['type'] == 'all':
        Protocols.alarm_on()
    elif (received_json['type'] == 'node') and ('node_id' in received_json):
        Protocols.send_cmd(received_json['node_id'], 'ON')
    else:
        status = -1
    return {"status": status, "body": json.dumps({'cmd': 'alarm_on'})}

@app.post('/alarm_off')
def post_alarm_off():
    if request.json is None:
        return {'error': 'No JSON request received'}, 500

    received_json = request.json
    print(f'[Web server] received {received_json}')
    status = 0
    if received_json['type'] == 'all':
        Protocols.alarm_off()
    elif (received_json['type'] == 'node') and ('node_id' in received_json):
        Protocols.send_cmd(received_json['node_id'], 'OFF')
    else:
        status = -1
    return {"status": status, "body": json.dumps({'cmd': 'alarm_off'})}

@app.post('/reset')
def post_reset():
    if request.json is None:
        return {'error': 'No JSON request received'}, 500

    received_json = request.json
    print(f'[Web server] received {received_json}')
    status = 0
    if received_json['type'] == 'all':
        Protocols.reset()
    elif (received_json['type'] == 'node') and ('node_id' in received_json):
        Protocols.send_cmd(received_json['node_id'], 'RESET')
    else:
        status = -1
    return {"status": status, "body": json.dumps({'cmd': 'reset'})}

