from api.models import Task
import json

def getTasksCount():
    """Returns a task count"""
    task_count = Task.objects.count()
    return task_count

def getFilteredTasksCount():
    """Returns a filtered task count"""
    task_count = Task.objects.filter(completion_status__exact=True).count()
    return task_count

def getTasksList(page, page_limit):
    """Returns a list of tasks, with pagination"""
    start_index = (page - 1) * page_limit
    end_index = start_index + page_limit
    tasks = Task.objects.all()[start_index:end_index]
    return tasks

def getFilteredTaskList(page, page_limit):
    """Returns a list of filtered tasks based on completion status"""
    start_index = (page - 1) * page_limit
    end_index = start_index + page_limit
    tasks = Task.objects.filter(completion_status__exact=True)[start_index:end_index]
    return tasks

def getTask(pkey):
    """Returns a task with details, from the given primary key (pkey)"""
    try:
        task = Task.objects.get(id=pkey)
    except Task.DoesNotExist:
        return None
    return task

def createTask(title, user, description = ""):
    """Creates a new task, with description being optional.
    Call save in the respective view in order to save to the DB"""
    task = Task(title=title, description=description, completion_status=False, user=user)
    return task

def parseUpdateTaskReq(request):
    """Parses a request for the update task endpoint only"""
    req_body = json.loads(request.body)
    if request.method == "PUT":
        title = req_body.get("title", None)
        description = req_body.get("description", "")
    elif request.method == "PATCH":
        title = req_body.get("title", None)
        description = req_body.get("description", "")
    else:
        title = None
        description = None
    
    return { "title": title, "description": description }
        

def updateTask(pkey, title = None, description = None):
    """Looks up a task then updates it, but doesn't save it on the DB.
    Call save in the respective view in order to save to the DB"""
    task = Task.objects.get(id=pkey)
    task.title, task.description = title, description
    return task