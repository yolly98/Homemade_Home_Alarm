from flask import Flask, request
from flask_cors import CORS
import json


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
    print(f'[Web server] received get status')
    return {"status": 0, "body": json.dumps({'cmd': 'status'})}


@app.post('/keep_alive')
def post_keep_alive():
    if request.json is None:
        return {'error': 'No JSON request received'}, 500

    received_json = request.json
    print(f'[Web server] received {received_json}')
    return {"status": 0, "body": json.dumps({'cmd': 'keep_alive'})}

@app.post('/alarm_on')
def post_alarm_on():
    if request.json is None:
        return {'error': 'No JSON request received'}, 500

    received_json = request.json
    print(f'[Web server] received {received_json}')
    return {"status": 0, "body": json.dumps({'cmd': 'alarm_on'})}

@app.post('/alarm_off')
def post_alarm_off():
    if request.json is None:
        return {'error': 'No JSON request received'}, 500

    received_json = request.json
    print(f'[Web server] received {received_json}')
    return {"status": 0, "body": json.dumps({'cmd': 'alarm_off'})}

@app.post('/reset')
def post_reset():
    if request.json is None:
        return {'error': 'No JSON request received'}, 500

    received_json = request.json
    print(f'[Web server] received {received_json}')
    return {"status": 0, "body": json.dumps({'cmd': 'reset'})}

@app.post('/send')
def post_send():
    if request.json is None:
        return {'error': 'No JSON request received'}, 500

    received_json = request.json
    print(f'[Web server] received {received_json}')
    return {"status": 0, "body": json.dumps({'cmd': 'send'})}
