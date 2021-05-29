from dataReader import DataReader
from flask import Flask, json, Response
from bson import json_util
from config import connectionStr

app = Flask("illumination monitor")
app.config["DEBUG"] = False

dataReader = DataReader(connectionStr)

@app.route('/data', methods=['GET'])
def home():
    result = []
    for doc in dataReader.getAllData():
        result.append({ "time": doc["time"].isoformat(), "value": doc["illumination"] })
    return Response(json.dumps({'data': result}, default=json_util.default),
                mimetype='application/json')

app.run()