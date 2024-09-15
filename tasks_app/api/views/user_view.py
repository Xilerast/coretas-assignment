from api.models import User
from api.serializers import UserSerializer
from django.http import Http404, JsonResponse, HttpResponse, HttpResponseBadRequest, HttpResponseServerError, HttpResponseForbidden
import json
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.decorators.csrf import csrf_exempt

def getUser(request):
    """Returns a single user. Available ONLY as GET."""
    if request.method != "GET":
        raise Http404
    
    id = request.GET.get("id", None)
    if id is None:
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

    if username is None or email is None or password is None:
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

@api_view(["POST"])
def loginUser(request):
    """Logs user in and returns a cookie with a JWT.
    Available ONLY as POST."""
    if request.method != "POST":
        raise Http404
    
    req_body = json.loads(request.body)
    username = req_body.get("username")
    password = req_body.get("password")

    user = authenticate(request=request, username=username, password=password)

    if user is not None:
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        response = Response(data={
            "access": str(access),
            "refresh": str(refresh)
        }, status=200, content_type="application/json")

        response.set_cookie(
            key="access",
            value=str(access),
            httponly=True,
            secure=False,
            samesite="Lax",
            max_age=3600
        )

        return response
    
    return HttpResponseForbidden(json.dumps({
            "success": False,
            "status": 403,
            "message": "Unauthorized. Invalid credentials."
        }), content_type="application/json")