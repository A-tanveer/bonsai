from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.db.models import F
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

from URL_Shortner.models import ShortenURL, URLVisits
from URL_Shortner.short_url import ShortUrl
import datetime

from django.views.decorators.csrf import csrf_protect
from django.template import loader, RequestContext


def index(request):
    url_error = False
    url_input = ''
    shortened_url = ''

    if request.method == 'POST':
        validator = URLValidator()
        # here presence of a second argument should be checked. if present this thing will be different
        try:
            url_input =request.POST.get('url', None)
            if not url_input:
                url_error = True
            else:
                validator(url_input)
        except ValidationError:
            url_error = True
        if not url_error:
            shortened_db = ShortenURL()
            short = ShortUrl()
            shortened_db.short_url = short.encode(shortened_db.id)
            shortened_db.url = url_input
            shortened_db.shortened_id = short.decode(shortened_db.short_url)
            shortened_db.save()
            shortened_url = request.build_absolute_uri(shortened_db.short_url)
            url_input = ''

    # template = loader.get_template('URL_Shortner/index.html')
    # render to response should be updated for django versions
    return render_to_response('URL_Shortner/index.html',
                              {'error':url_error, 'url':url_input, 'short_url':shortened_url},
                              context=request)


def redirect_url(request, short):

    print(short)

    url_obj = get_object_or_404(ShortenURL, short_url=short)

    ShortenURL.objects.filter(short_url=short).update(hits=F('hits')+1)

    if not URLVisits.objects.filter(url_id_fk=url_obj, visit_date=datetime.date.today()).exists():
        x = URLVisits()
        x.from_country = "Get country from IP and insert here"
        x.visit_date = datetime.date.today()
        x.referral = 'Get referral web domain name'
        x.url_id_fk = url_obj
        x.save()

    URLVisits.objects.filter(url_id_fk=url_obj, visit_date=datetime.date.today).update(hits=F('hits')+1)

    return redirect(url_obj.url)


def stats(request, short):
    short_db = get_object_or_404(ShortenURL, short_url=short)

    stats = URLVisits.objects.filter(day__gt=datetime.date.today()-datetime.timedelta(days=30),
                                     url_id_fk=short_db).all()

    link_url = request.build_absolute_uri("/" + short_db.short_url)  # make it an absolute one

    # render to response should be updated for django versions
    return render_to_response("stats.html", {"stats": stats, "link": short_db, "link_url": link_url},
                              context_instance=RequestContext(request))


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
