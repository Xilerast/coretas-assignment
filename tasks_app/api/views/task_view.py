from api.utils import task_utils
from django.http import Http404, JsonResponse, HttpResponseServerError, HttpResponseBadRequest, HttpResponseNotFound
from api.serializers import TaskSerializer
from api.models import Task
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes, api_view
import json

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getTasks(request):
    """Gets a list of tasks from the DB, and returns a JSON containing said list.
    Available ONLY as a GET request"""
    if request.method != "GET":
        raise Http404
    
    page = int(request.GET.get("page", 1))
    page_size = int(request.GET.get("page_size", 10))
    filtered = request.GET.get("filtered", 0)
    user = request.user
    if filtered == 0:
        tasks = task_utils.getTasksList(page=page, page_limit=page_size, user=user)
        tasks_number = task_utils.getTasksCount(user=user)
    else:
        tasks = task_utils.getFilteredTaskList(page=page, page_limit=page_size, user=user)
        tasks_number = task_utils.getFilteredTasksCount(user=user)
    serializer = TaskSerializer(tasks, many=True)
    return JsonResponse({
        "tasks": serializer.data,
        "tasks_number": tasks_number
    })

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getTask(request, pkey):
    """Gets a single task from the DB, with the given Primary Key on the
    GET request. Available ONLY as a GET request"""
    if request.method != "GET":
        raise Http404
    
    task = task_utils.getTask(pkey=pkey)
    if task is None:
        return HttpResponseNotFound(json.dumps({
            "success": False,
            "status": 404,
            "message": "Not found"
        }), content_type="application/json")

    return JsonResponse(TaskSerializer(task, many=False).data)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def createTask(request):
    """Creates a single task and inserts it on the DB.
    Available ONLY as a POST request"""
    if request.method != "POST":
        raise Http404
    
    req_body = json.loads(request.body)
    title = req_body.get("title")
    if title == None:
        return HttpResponseBadRequest(json.dumps({
            "success": False,
            "status": 400,
            "message": "Bad request"
        }), content_type="application/json")
    
    description = req_body.get("description", "")

    task = task_utils.createTask(title=title, description=description, user=request.user)

    try:
        task.save()
    except Exception as e:
        return HttpResponseServerError(json.dumps({
            "success": False,
            "status": 500,
            "message": "Internal Server Error. Could not insert new task in DB."
        }), content_type="application/json")
    
    return JsonResponse(TaskSerializer(task, many=False).data)

@api_view(["PUT", "PATCH"])
@permission_classes([IsAuthenticated])
def updateTask(request, pkey):
    """Updates a task and saves it on the DB.
    Available ONLY as a PUT/PATCH request."""
    if request.method != "PUT" and request.method != "PATCH":
        raise Http404
    
    parsedReq = task_utils.parseUpdateTaskReq(request=request)

    id = pkey
    title = parsedReq.get("title")
    description = parsedReq.get("description")
    
    if id == None or title == None:
        return HttpResponseBadRequest(json.dumps({
            "success": False,
            "status": 400,
            "message": "Bad request"
        }), content_type="application/json")
    
    task = task_utils.updateTask(pkey=id, title=title, description=description)

    try:
        task.save()
    except Exception as e:
        return HttpResponseServerError(json.dumps({
            "success": False,
            "status": 500,
            "message": "Internal Server Error. Could not update task in DB."
        }), content_type="application/json")
    
    return JsonResponse(TaskSerializer(task, many=False).data)

@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def completeTask(request, pkey):
    """Completes a task and saves it on the DB.
    Available ONLY as PATCH request."""
    if request.method != "PATCH":
        raise Http404
    
    id = pkey

    if id == None:
        return HttpResponseBadRequest(json.dumps({
            "success": False,
            "status": 400,
            "message": "Bad request"
        }), content_type="application/json")
    
    task = Task.objects.get(id=id)
    if task == None:
        return HttpResponseNotFound(json.dumps({
            "success": False,
            "status": 404,
            "message": "Not found"
        }), content_type="application/json")
    
    task.completion_status = True
    
    try:
        task.save()
    except:
        return HttpResponseServerError(json.dumps({
            "success": False,
            "status": 500,
            "message": "Internal Server Error. Could not update task in DB."
        }), content_type="application/json")
    
    return JsonResponse(TaskSerializer(task, many=False).data)

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def deleteTask(request, pkey):
    """Deletes a task from the DB.
    Available ONLY as a DELETE request."""
    if request.method != "DELETE":
        raise Http404
    
    id = pkey
    if id == None:
        return HttpResponseBadRequest(json.dumps({
            "success": False,
            "status": 400,
            "message": "Bad Request"
        }), content_type="application/json")
    
    try:
        task = Task.objects.get(id=id)
    except Task.DoesNotExist:
        return HttpResponseNotFound(json.dumps({
            "success": False,
            "status": 404,
            "message": "Not found"
        }), content_type="application/json")
    
    try:
        task.delete()
    except:
        return HttpResponseServerError(json.dumps({
            "success": False,
            "status": 500,
            "message": "Internal Server Error. Could not delete task from DB."
        }), content_type="application/json")
    finally:
        return JsonResponse({
            "success": True,
            "status": 200,
            "message": "OK"
        })
