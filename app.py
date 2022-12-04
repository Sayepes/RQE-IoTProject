import pymongo as pymongo
from flask import Flask, request, jsonify
# from flask_objectid_converter import ObjectIDConverter
from pymongo import ReturnDocument
from pymongo.server_api import ServerApi
from Schemas import ReadingSchemaPost, CompareSchemaPost
from bson import json_util, ObjectId
# from flask_cors import CORS
# loading private connection information from environment variables
# from dotenv import load_dotenv
# load_dotenv()
import os

MONGODB_LINK = os.environ.get("MONGODB_LINK")
MONGODB_USER = os.environ.get("MONGODB_USER")
MONGODB_PASS = os.environ.get("MONGODB_PASS")

# Connecting to mongodb
client = pymongo.MongoClient(
    f"mongodb+srv://carstaltari:Pablo__545@iot2-carlo.ijsiznf.mongodb.net/?retryWrites=true&w=majority",
    server_api=ServerApi('1'))
# Name of database
db = client.todoitem_sec1

app = Flask(__name__)


# New reading from arduino
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
    # Validate JSON Object
    # Schema Validation
    error = ReadingSchemaPost().validate(reading)
    if error:
        return error, 400

    # Parse JSON object --NOT NEEDED
    coll_id = reading["collection_id"]
    time = reading["time"]
    temp = reading["temp"]
    humi = reading["humi"]
    lumi = reading["lumi"]

    # Write to DB
    # Insert into db (coll_id, time, temp, humi, lumi)
    try:
        inserted_id = db.reading.insert_one(reading).inserted_id
        reading["_id"] = str(inserted_id)
        return jsonify(reading)

    except Exception as e:
        return {"error": "some error happened"}, 500


# Get readings from DB
@app.route('/collection/<collection_id>', methods=["GET"])
def get_readings_from_collection(collection_id):
    # Select from results DB using collection_id
    try:
        cursor = db.results.find({"collection_id": collection_id})
        readings = list(cursor)
        for reading in readings:
            if "_id" in reading:
                reading["_id"] = str(reading["_id"])

        # Return readings from query
        return jsonify(readings)
    except Exception as e:
        print(e)
        return {"error": "some error happened"}, 501


# Delete collection & all readings from collection in DB
@app.route("/collection/<collection_id>", methods=["DELETE"])
def delete_collection(collection_id):
    try:
        # Delete collection from collection table
        deleted_collection = db.collections.find_one_and_delete({"_id": ObjectId(collection_id)},
                                                                projection={"_id": False})
        if deleted_collection is None:
            return {"error": "Collection not found"}, 404
        if "_id" in deleted_collection:
            deleted_collection["_id"] = str(deleted_collection["_id"])

        # Delete readings from reading table
        deleted_readings = db.results.delete_many({"collection_id": collection_id})
        print(deleted_readings.deleted_count, " readings deleted")

        # Return deleted readings
        return jsonify(deleted_readings)

    except Exception as e:
        return {"error": "some error happened"}, 501


# Compare data collection with inserted data
@app.route("/collection/<collection_id>/compare/<temp>/<humi>/<lumi>", methods=["GET"])
def compare_collection(collection_id, temp, humi, lumi):
    avg_temp = None
    avg_humi = None
    avg_lumi = None

    temp_rating = 0
    humi_rating = 0
    lumi_rating = 0

    return_msg = {}

    # Select from collection DB using collection_id
    try:
        cursor = db.collection.find({"collection_id": collection_id})
        readings = list(cursor)
        for reading in readings:
            if "_id" in reading:
                reading["_id"] = str(reading["_id"])
            # assign values from avg pipelines
            avg_temp = reading["avgTemp"]
            avg_humi = reading["avgHumi"]
            avg_lumi = reading["avgLumi"]

        if temp.isnumeric():
            if humi.isnumeric():
                if lumi.isnumeric():
                    # Calculate Percentage Rating
                    temp_rating = (avg_temp / temp) * 100
                    humi_rating = (avg_humi / humi) * 100
                    lumi_rating = (avg_lumi / lumi) * 100

                    return_msg = {"Temperature": "{:.2f}%".format(temp_rating, ),
                                  "Humidity": "{:.2f}%".format(humi_rating),
                                  "Luminosity": "{:.2f}%".format(lumi_rating)}

                    # Return Grade Percentage for all values
                    return jsonify(return_msg)
                else:
                    # Return Message for invalid luminosity value
                    return {"error": "Invalid Data for Luminosity"}, 400
            else:
                # Return Message for invalid humidity value
                return {"error": "Invalid Data for Humidity"}, 400
        else:
            # Return Message for invalid temperature value
            return {"error": "Invalid Data for Temperature"}, 400

        # Return readings from query
        # return jsonify(readings)
    except Exception as e:
        print(e)
        return {"error": "some error happened"}, 501


# Compare data collection with JSON Object
@app.route("/collection/<collection_id>/compare/", methods=["POST"])
def compare_collection_JSON(collection_id):
    # JSON Object Template
    # {
    #     "temp": 22.33,
    #     "humi": 10.43,
    #     "lumi": 67.32
    # }
    # Get JSON Object
    reading = request.json
    # Schema Validation
    error = CompareSchemaPost().validate(reading)
    if error:
        return error, 400

    # Parse JSON object
    temp = reading["temp"]
    humi = reading["humi"]
    lumi = reading["lumi"]

    avg_temp = None
    avg_humi = None
    avg_lumi = None

    temp_rating = 0
    humi_rating = 0
    lumi_rating = 0

    return_msg = {}

    # Select from collection DB using collection_id
    try:
        cursor = db.collection.find({"collection_id": collection_id})
        readings = list(cursor)
        for reading in readings:
            if "_id" in reading:
                reading["_id"] = str(reading["_id"])
            # assign values from avg pipelines
            avg_temp = reading["avgTemp"]
            avg_humi = reading["avgHumi"]
            avg_lumi = reading["avgLumi"]

        if temp.isnumeric():
            if humi.isnumeric():
                if lumi.isnumeric():
                    # Calculate Percentage Rating
                    temp_rating = (avg_temp / temp) * 100
                    humi_rating = (avg_humi / humi) * 100
                    lumi_rating = (avg_lumi / lumi) * 100

                    return_msg = {"Temperature": "{:.2f}%".format(temp_rating),
                                  "Humidity": "{:.2f}%".format(humi_rating),
                                  "Luminosity": "{:.2f}%".format(lumi_rating)}

                    # Return Grade Percentage for all values
                    return jsonify(return_msg)
                else:
                    # Return Message for invalid luminosity value
                    return {"error": "Invalid Data for Luminosity"}, 400
            else:
                # Return Message for invalid humidity value
                return {"error": "Invalid Data for Humidity"}, 400
        else:
            # Return Message for invalid temperature value
            return {"error": "Invalid Data for Temperature"}, 400

        # Return readings from query
        # return jsonify(readings)
    except Exception as e:
        print(e)
        return {"error": "some error happened"}, 501


# Compare data collection with JSON Object
@app.route("/comparetest", methods=["POST"])
def compare_test():
    # JSON Object Template
    # {
    #     "temp": "22.33",
    #     "humi": "10.43",
    #     "lumi": "67.32"
    # }
    # Get JSON Object
    reading = request.json
    # Schema Validation
    error = CompareSchemaPost().validate(reading)
    if error:
        return error, 400

    # Parse JSON object
    temp = reading["temp"]
    humi = reading["humi"]
    lumi = reading["lumi"]

    avg_temp = 27
    avg_humi = 10
    avg_lumi = 71

    temp_rating = 0
    humi_rating = 0
    lumi_rating = 0

    return_msg = {}

    # Select from collection DB using collection_id
    try:
        if temp:
            if humi:
                if lumi:
                    # Calculate Percentage Rating
                    temp_rating = (avg_temp / temp) * 100
                    humi_rating = (avg_humi / humi) * 100
                    lumi_rating = (avg_lumi / lumi) * 100

                    return_msg = {"Temperature": "{:.2f}%".format(temp_rating),
                                  "Humidity": "{:.2f}%".format(humi_rating),
                                  "Luminosity": "{:.2f}%".format(lumi_rating)}

                    # Return Grade Percentage for all values
                    return jsonify(return_msg)
                else:
                    # Return Message for invalid luminosity value
                    return {"error": "Invalid Data for Luminosity"}, 400
            else:
                # Return Message for invalid humidity value
                return {"error": "Invalid Data for Humidity"}, 400
        else:
            # Return Message for invalid temperature value
            return {"error": "Invalid Data for Temperature"}, 400

        # Return readings from query
        # return jsonify(readings)
    except Exception as e:
        print(e)
        return {"error": "some error happened"}, 501


if __name__ == '__main__':
    app.run()
