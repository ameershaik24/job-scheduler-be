import json
from mongoengine import connect
from datetime import datetime

connection = connect(alias='seed-connection')
db = connection['mainapplication']

with open("requests.json") as fp:
    data = json.load(fp)

db.create_collection("requests")
db.requests.insert_many(data, ordered=False)
db.requests.update_many({}, {"$set":{"updated":datetime.utcnow()}})