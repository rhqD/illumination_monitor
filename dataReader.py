import pymongo

class DataReader:
    def __init__(self, connectionStr):
        self.connectionStr = connectionStr
        self.connect()
    
    def connect(self):
        self.mongoClient = pymongo.MongoClient(self.connectionStr)
        self.dailyLogDB = self.mongoClient["daily_log"]
        self.pcf8591Log = self.dailyLogDB["pcf8591"]

    def getAllData(self):
        try:
            return self.pcf8591Log.find()
        except TimeoutError:
            self.connect()
            self.getAllData()

    def insertData(self, data):
        try:
            return self.pcf8591Log.insert_one(data)
        except TimeoutError:
            self.connect()
            self.insertData(data)
        