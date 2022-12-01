import pymongo as pymongo
from flask import Flask, request, jsonify
# from flask_objectid_converter import ObjectIDConverter
from pymongo import ReturnDocument
from pymongo.server_api import ServerApi
from Schemas import ReadingSchemaPost
from bson import json_util, ObjectId
# from flask_cors import CORS
app = Flask(__name__)

#New reading from arduino
@app.route('/read', methods=["POST"])
def add_new_reading():
    # JSON Object Template
    # {
    #     "collection_id": "00000000000",
    #     "time": "2022-02-02 14:32",
    #     "temp": "22.33",
    #     "humi": "10.43",
    #     "lumi": "67.32"
    # }
    # Get JSON Object
    reading = request.json
    #Validate JSON Object
    #Schema Validation
    error = ReadingSchemaPost().validate(reading)
    if error:
        return error, 400

    #Parse JSON object
    coll_id = reading["collection_id"]
    time = reading["time"]
    temp = reading["temp"]
    humi = reading["humi"]
    lumi = reading["lumi"]

    #Write to DB
    # insert into db (coll_id, time, temp, humi, lumi)

    #Return Success
    return "Successful Log Inserted"

if __name__ == '__main__':
    app.run()
