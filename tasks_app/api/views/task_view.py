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
    if filtered == 0:
        tasks = task_utils.getTasksList(page=page, page_limit=page_size)
        tasks_number = task_utils.getTasksCount()
    else:
        tasks = task_utils.getFilteredTaskList(page=page, page_limit=page_size)
        tasks_number = task_utils.getFilteredTasksCount()
    serializer = TaskSerializer(tasks, many=True)
    return JsonResponse({
        "tasks": serializer.data,
        "tasks_number": tasks_number
    })

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getTask(request):
    """Gets a single task from the DB, with the given Primary Key on the
    GET request. Available ONLY as a GET request"""
    if request.method != "GET":
        raise Http404
    
    id = request.GET.get("id", None)
    if id == None:
        return HttpResponseNotFound(json.dumps({
            "success": False,
            "status": 404,
            "message": "Not found"
        }), content_type="application/json")
    
    task = task_utils.getTask(pkey=id)

    return JsonResponse(TaskSerializer(task, many=False))

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def createTask(request):
    """Creates a single task and inserts it on the DB.
    Available ONLY as a POST request"""
    if request.method != "POST":
        raise Http404
    
    title = request.POST.get("title", None)
    if title == None:
        return HttpResponseBadRequest(json.dumps({
            "success": False,
            "status": 400,
            "message": "Bad request"
        }), content_type="application/json")
    
    description = request.POST.get("description", "")

    task = task_utils.createTask(title=title, description=description)

    try:
        task.save()
    except:
        return HttpResponseServerError(json.dumps({
            "success": False,
            "status": 500,
            "message": "Internal Server Error. Could not insert new task in DB."
        }), content_type="application/json")
    
    return JsonResponse(TaskSerializer(task, many=False))

@api_view(["PUT", "PATCH"])
@permission_classes([IsAuthenticated])
def updateTask(request):
    """Updates a task and saves it on the DB.
    Available ONLY as a PUT/PATCH request."""
    if request.method != "PUT" and request.method != "PATCH":
        raise Http404
    
    parsedReq = task_utils.parseUpdateTaskReq(request=request)

    id = parsedReq.get("id")
    title = parsedReq.get("title")
    description = parsedReq.get("description")
    
    if id == None or title == None:
        return HttpResponseBadRequest(json.dumps({
            "success": False,
            "status": 400,
            "message": "Bad request"
        }), content_type="application/json")
    
    task = task_utils.updateTask(id=id, title=title, description=description)

    try:
        task.save()
    except:
        return HttpResponseServerError(json.dumps({
            "success": False,
            "status": 500,
            "message": "Internal Server Error. Could not update task in DB."
        }), content_type="application/json")
    
    return JsonResponse(TaskSerializer(task, many=False))

@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def completeTask(request):
    """Completes a task and saves it on the DB.
    Available ONLY as PATCH request."""
    if request.method != "PATCH":
        raise Http404
    
    id = request.PATCH.get("id", None)

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
    
    task = task_utils.updateTask(pkey=task.id, title=task.title, description=task.description, completion_status=True)
    
    try:
        task.save()
    except:
        return HttpResponseServerError(json.dumps({
            "success": False,
            "status": 500,
            "message": "Internal Server Error. Could not update task in DB."
        }), content_type="application/json")
    
    return JsonResponse(TaskSerializer(task, many=False))

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def deleteTask(request):
    """Deletes a task from the DB.
    Available ONLY as a DELETE request."""
    if request.method != "DELETE":
        raise Http404
    
    id = request.DELETE.get("id", None)
    if id == None:
        return HttpResponseBadRequest(json.dumps({
            "success": False,
            "status": 400,
            "message": "Bad Request"
        }), content_type="application/json")
    
    task = Task.objects.get(id=id)
    if task == None:
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
