from django import http

def health(request):
    return http.HttpResponse()