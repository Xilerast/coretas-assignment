from api.models import User
from api.serializers import UserSerializer
from django.http import Http404, JsonResponse, HttpResponse, HttpResponseBadRequest, HttpResponseServerError
import json
from django.conf import settings
from django.contrib.auth.hashers import make_password

def getUser(request):
    """Returns a single user. Available ONLY as GET."""
    if request.method != "GET":
        raise Http404
    
    id = request.GET.get("id", None)
    if id == None:
        return HttpResponseBadRequest(json.dumps({
            "success": False,
            "status": 400,
            "message": "Bad request"
        }), content_type="application/json")
    
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
        return HttpResponseBadRequest(json.dumps({
            "success": False,
            "status": 400,
            "message": "Bad request"
        }), content_type="application/json")
    
    password_confirm = req_body.get("password_confirm")

    if password != password_confirm:
        return HttpResponseBadRequest(json.dumps({
            "success": False,
            "status": 400,
            "message": "Bad request. Passwords do not match."
        }), content_type="application/json")

    first_name = req_body.get("first_name")
    last_name = req_body.get("last_name")

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        user = None
    else:
        return HttpResponse(json.dumps({
            "success": False,
            "status": 409,
            "message": "Conflict: Resource already exists"
        }), status=409, content_type="application/json")
    
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        user = None
    else:
        return HttpResponse(json.dumps({
            "success": False,
            "status": 409,
            "message": "Conflict: Resource already exists"
        }), status=409, content_type="application/json")

    try:
        user = User.objects.create(username=username, email=email, password=make_password(password), first_name=first_name, last_name=last_name)
    except:
        if settings.DEBUG == True:
            raise
        return HttpResponseServerError(json.dumps({
            "success": False,
            "status": 500,
            "message": "Internal Server Error. Could not insert new user in DB."
        }), content_type="application/json")
    
    return HttpResponse(json.dumps({
        "success": True,
        "status": 201,
        "message": "Created"
    }), status=201, content_type="application/json")