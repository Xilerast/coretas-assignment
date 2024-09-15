from django.http import Http404, JsonResponse
from django.middleware.csrf import get_token

def default(request):
    """Default endpoint for API. Does nothing except confirm API is working."""
    if request.method != "GET":
        raise Http404
    
    return JsonResponse({
        "status": "OK"
    })

def csrf(request):
    return JsonResponse({'csrfToken': get_token(request)})