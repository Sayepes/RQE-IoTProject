import pymongo as pymongo
from flask import Flask, request, jsonify
# from flask_objectid_converter import ObjectIDConverter
from pymongo import ReturnDocument
from pymongo.server_api import ServerApi
# from Schemas import ToDoItemSchemaPut, ToDoItemSchemaPost, ToDoItemsSchemaPatch
from bson import json_util, ObjectId
# from flask_cors import CORS
app = Flask(__name__)

#New reading from arduino
@app.route('/read', methods=["POST"])
def add_new_reading():
    # JSON Object Template
    # {
    #     "collection_id": "dsdsdddsd",
    #     "time": "2022-02-02 14:32",
    #     "temp": "22.33",
    #     "humi": "10.43",
    #     "lumi": "67.32"
    # }
    # Get JSON Object
    reading = request.json
    #Validate JSON Object
    #Schema Validation
    error = False
    if error:
        return error, 400
    #Parse JSON object

    #Write to DB

    #Return Success
    return "Complete"

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
