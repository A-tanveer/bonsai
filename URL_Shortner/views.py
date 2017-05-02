from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from URL_Shortner.models import ShortenURL, URLVisits
from URL_Shortner.short_url import ShortUrl
from django.views.decorators.csrf import csrf_protect
from django.template import loader


def index(request):
    # c = {}
    # c.update(csrf_protect)
    template = loader.get_template('URL_Shortner/index.html')
    return HttpResponse(template.render())


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
    url = request.POST.get('url', '')
    # if url==VALID_URL:
    #     id = insert url into DB and get its id
    #     short_obj = ShortUrl()
    #     string = short_obj(id)
    #     insert into DB
    #     show shortened url
    return HttpResponse("short this URL")


def custom_url(reuest):
    url, custom = reuest.POST.get('url', 'custom', '')
    short_obj = ShortUrl()
    short_id = short_obj.decode(custom)
    # if short_id not in DB
        # if url==VALID_URL:
        #     insert into DB
        #     return url
