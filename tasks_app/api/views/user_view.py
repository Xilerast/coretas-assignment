from api.models import User
from api.serializers import UserSerializer
from django.http import Http404, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.conf import settings
from django.contrib.auth.hashers import make_password

def getUser(request):
    """Returns a single user. Available ONLY as GET."""
    if request.method != "GET":
        raise Http404
    
    id = request.GET.get("id", None)
    if id == None:
        return JsonResponse({
            "success": False,
            "status": 400,
            "message": "Bad request"
        })
    
    user = User.objects.get(id=id)

    return JsonResponse(UserSerializer(user, many=False))

def registerUser(request):
    """Registers user. Creates and adds user to DB.
    Available ONLY as POST."""
    if request.method != "POST":
        raise Http404
    
    req_body = json.loads(request.body)
    username = req_body.get("username")
    email = req_body.get("email")
    password = req_body.get("password")

    if username == None or email == None or password == None:
        return JsonResponse({
            "success": False,
            "status": 400,
            "message": "Bad request"
        })
    
    first_name = request.POST.get("first_name", None)
    last_name = request.POST.get("last_name", None)

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        user = None
    else:
        return JsonResponse({
            "success": False,
            "status": 409,
            "message": "Conflict: Resource already exists"
        })
    
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        user = None
    else:
        return JsonResponse({
            "success": False,
            "status": 409,
            "message": "Conflict: Resource already exists"
        })

    try:
        user = User.objects.create(username=username, email=email, password=make_password(password), first_name=first_name, last_name=last_name)
    except:
        if settings.DEBUG == True:
            raise
        return JsonResponse({
            "success": False,
            "status": 500,
            "message": "Internal Server Error. Could not insert new user in DB."
        })
    
    return JsonResponse({
        "success": True,
        "status": 201,
        "message": "Created"
    })