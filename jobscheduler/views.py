import json
import traceback
from datetime import datetime
from mongoengine import connect
from bson.objectid import ObjectId
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view

from . import tasks
from .models import *
from .exceptions import *

connect('mainapplication')

@api_view(["GET"])
def get_jobs_requested(request):
    try:
        return HttpResponse(tasks.get_all_jobs())
    except Exception as err:
        traceback.print_exc()
        return HttpResponse(json.dumps({
                                       "msg":"Error occured during fetching jobs - " + str(err)
                                       }
                                       ),status=500)


@api_view(["POST"])
def create_job(request):
    try:
        if ({"name", "request_details", "request_interval_seconds"} - set(request.data.keys())):
            raise ValidationError("All request params", "are not present")

        name = request.data.get('name')
        if not name:
            raise ValidationError("Name", "cannot be empty")

        notifications = request.data.get('notifications', {"phones": [], "emails": []})
        request_details = json.loads(request.data.get('request_details'))
        if not request_details["url"]:
            raise ValidationError("Endpoint", "cannot be empty")

        request_interval_seconds = int(request.data.get('request_interval_seconds')[:-8])
        tolerated_failures = request.data.get('tolerated_failures', None)

        request_object = Requests(
                                  name = name,
                                  notifications = json.loads(notifications),
                                  request = request_details,
                                  request_interval_seconds = request_interval_seconds,
                                  tolerated_failures = tolerated_failures
                                  )
        request_object.save()
        return HttpResponse("Created the job successfully", status=200)
    except ValidationError as err:
        return HttpResponse(json.dumps({
                                       "msg":"Validation failed | " + err.validation + " - " + err.message
                                       }
                                       ),status=400)
    except Exception as err:
        traceback.print_exc()
        return HttpResponse(json.dumps({
                                       "msg":"Error occured during job creation - " + str(err)
                                       }
                                       ),status=500)

@api_view(["DELETE"])
def delete_job(request, pk):
    try:
        Requests.objects(__raw__={'_id': ObjectId(pk)}).delete()
        return HttpResponse(json.dumps({
                                       "msg":"Deleted the job successfully"
                                       }), status=200)
    except Exception as err:
        traceback.print_exc()
        return HttpResponse(json.dumps({
                                       "msg":"Error occured during job deletion - " + str(err)
                                       }
                                       ),status=500)

@api_view(["PUT"])
def pause_play_job(request, pk, is_paused):
    try:
        request_object = Requests.objects(__raw__={'_id': ObjectId(pk)})
        if is_paused=="no":
            new_status = "Paused"
        else:
            new_status = "Resumed"

        request_object.update(
                              set__status=new_status,
                              set__updated=datetime.utcnow()
                              )
        return HttpResponse(json.dumps({
                                       "msg": new_status + " the job successfully"
                                       }), status=200)
    except Exception as err:
        traceback.print_exc()
        return HttpResponse(json.dumps({
                                       "msg":"Error occured during pausing the job - " + str(err)
                                       }
                                       ),status=500)


