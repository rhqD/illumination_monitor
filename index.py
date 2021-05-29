from pcf8951 import PCF8591
from werkzeug.utils import send_file
from dataReader import DataReader
from flask import Flask, json, Response, send_from_directory
from bson import json_util
from config import connectionStr
import atexit
from smbus import SMBus
from flask_cors import CORS, cross_origin
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask("illumination monitor", static_folder='monitor/build')
CORS(app, support_credentials=True)
app.config["DEBUG"] = False

dataReader = DataReader(connectionStr)
pcf8591 = PCF8591(SMBus(1))

def collectData():
    data = pcf8591.read()
    dataReader.insertData(data)

scheduler = BackgroundScheduler()
scheduler.add_job(func=collectData, trigger="interval", seconds=600)
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

@app.route('/data', methods=['GET'])
@cross_origin(supports_credentials=True)
def home():
    result = []
    for doc in dataReader.getAllData():
        result.append({ "time": doc["time"].isoformat(), "value": doc["illumination"] })
    return Response(json.dumps({'data': result}, default=json_util.default),
                mimetype='application/json')

@app.route('/monitor/<path:path>')
def serve_monitor(path):
    return send_from_directory("monitor/build", path)

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory("monitor/build/static", path)

@app.route('/<path:filename>')
def serve_root(filename):
    return send_from_directory("monitor/build", filename)

@app.errorhandler(404)
def page_not_found(e):
    print("fuck")
    return app.send_static_file("index.html"), 200


app.run(port=5000, host="0.0.0.0")