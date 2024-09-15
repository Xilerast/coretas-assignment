from api.models import Task

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
    task = Task.objects.get(id=pkey)
    return task

def createTask(title, description = ""):
    """Creates a new task, with description being optional.
    Call save in the respective view in order to save to the DB"""
    task = Task(title=title, description=description, completion_status=False)
    return task

def parseUpdateTaskReq(request):
    """Parses a request for the update task endpoint only"""
    if request.method == "PUT":
        id = request.PUT.get("id", None)
        title = request.PUT.get("title", None)
        description = request.PUT.get("description", "")
    elif request.method == "PATCH":
        id = request.PATCH.get("id", None)
        title = request.PATCH.get("title", None)
        description = request.PATCH.get("description", "")
    else:
        id = None
        title = None
        description = None
    
    return { "id": id, "title": title, "description": description }
        

def updateTask(pkey, title = None, description = None, completion_status = None):
    """Looks up a task then updates it, but doesn't save it on the DB.
    Call save in the respective view in order to save to the DB"""
    task = Task.objects.get(id=pkey)
    task.title, task.description, task.completion_status = title, description, completion_status
    return task