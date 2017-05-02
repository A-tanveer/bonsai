from django.http import HttpResponse


def index(request):
    return HttpResponse("This is Shortner index")


def short_url(request):
    return HttpResponse("redirect to long url")


def shortened_form(request):
    return HttpResponse("View shortened url")
