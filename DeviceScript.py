import requests
import json

# Script to Emulate data from device

request_url = "http://127.0.0.1:5000"

compareTestUrl = request_url + "/compareTest"

device_id = "000000"
collection_id = "000222"
record_id = "0029292"

lumi = 60
humi = 14.21
temp = 21.32

running = False

collectionStatus = input("Press y to send request")

if collectionStatus == "Y":
    running = True

if running:
    reading = {
        "record_id": record_id,
        "device_id": device_id,
        "collection_id": collection_id,
        "humi": humi,
        "lumi": lumi,
        "temp": temp
    }
    requests.post(compareTestUrl, reading)

