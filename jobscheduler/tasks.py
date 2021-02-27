import json
from mongoengine import connect
import datetime

connection = connect(alias='second-connection')
db = connection['mainapplication']

def convert_timedelta(duration):
    days, seconds = duration.days, duration.seconds
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = (seconds % 60)
    return days, hours, minutes, seconds

def get_status_update_string(request_time, updated_time):
    days, hours, minutes, seconds = convert_timedelta(request_time-updated_time)
    r = ""
    if days:
        r += str(days) + " d, "
    if hours:
        r += str(hours) + " hr, "
    if minutes:
        r += str(minutes) + " min, "
    if seconds:
        r += str(seconds) + " sec "

    print("===========================")
    print(r)
    if r:
        if r[-2] == ",":
            r = r[:-2] + " ago"
        else:
            r += " ago"
    else:
        r = "1 sec ago"
    return r

def get_all_jobs():
    cursor = db['requests'].find().sort("updated", -1)
    list_of_requests = []
    time_now = datetime.datetime.utcnow()
    for doc in cursor:
        time_since_update = get_status_update_string(time_now, doc["updated"])
        doc["status"] = doc["status"] + " " + time_since_update
        doc["_id"] = str(doc["_id"])
        doc["updated"] = str(doc["updated"])
        list_of_requests.append(doc)
    return json.dumps(list_of_requests)


