from django.http import Http404, JsonResponse, HttpResponse
from django.middleware.csrf import get_token

def default(request):
    """Default endpoint for API. Does nothing except confirm API is working."""
    if request.method != "GET":
        raise Http404
    
    return JsonResponse({
        "status": "OK"
    })

def csrf(request):
    token = get_token(request=request)
    return JsonResponse({
        "csrfToken": token
    })