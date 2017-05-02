from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from URL_Shortner.models import ShortenURL, URLVisits
from URL_Shortner.short_url import ShortUrl


def index(request):
    # c = {}
    # c.update(cs)
    return HttpResponse("This is Shortner index")


def short_url(request, short):
    short_id = ShortUrl.decode(short)
    url_obj = get_object_or_404(ShortenURL, shortened_id=short_id)
    url = url_obj.url
    str = "redirect to long url: " + short
    return HttpResponse(str)


def shortened_form(request):
    return HttpResponse("View shortened url")

