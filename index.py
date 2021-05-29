from pcf8951 import PCF8591
from dataReader import DataReader
from flask import Flask, json, Response
from bson import json_util
from config import connectionStr
import atexit
from smbus import SMBus

from apscheduler.schedulers.background import BackgroundScheduler

app = Flask("illumination monitor")
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
def home():
    result = []
    for doc in dataReader.getAllData():
        result.append({ "time": doc["time"].isoformat(), "value": doc["illumination"] })
    return Response(json.dumps({'data': result}, default=json_util.default),
                mimetype='application/json')

app.run(port=5000, host="0.0.0.0")