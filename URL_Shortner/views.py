from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from URL_Shortner.models import ShortenURL, URLVisits
from URL_Shortner.short_url import ShortUrl


def index(request):
    # c = {}
    # c.update(cs)
    return HttpResponse("This is Shortner index")


def redirect_url(request, short):
    short_obj = ShortUrl()
    short_id = short_obj.decode(short)
    url_obj = get_object_or_404(ShortenURL, shortened_id=short_id)
    url = url_obj.url
    # str = "redirect to long url: " + short
    return HttpResponseRedirect(url)


def shortened_form(request):
    return HttpResponse("View shortened url")


def sorten_url(request):
    return HttpResponse("short this URL")