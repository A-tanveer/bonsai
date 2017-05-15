import datetime

from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.db.models import F
from django.shortcuts import get_object_or_404, render_to_response, redirect, render
from django.template import RequestContext

from URL_Shortner.models import ShortenURL, URLVisits
from URL_Shortner.short_url import ShortUrl


# from django.contrib.gis.geoip import GeoIP


def index(request):
    url_error = False
    custom_error = False
    char_err = False
    url_input = ''
    shortened_url = ''

    if request.method == 'POST':
        validator = URLValidator()
        # here presence of a second argument should be checked. if present this thing will be different
        try:
            url_input =request.POST.get('url', None)
            custom_short = request.POST.get('custom', None)
            if not url_input:
                url_error = True
            else:
                validator(url_input)
        except ValidationError:
            url_error = True
        if not url_error:
            shortened_db = ShortenURL()
            short = ShortUrl()
            shortened_db.url = url_input
            if not custom_short:
                shortened_db.save()
                shortened_db.short_url = short.encode(shortened_db.id)  # custom url isn't yet supported
                shortened_db.shortened_id = short.decode(shortened_db.short_url)
                shortened_db.save()
                shortened_url = request.build_absolute_uri(shortened_db.short_url)
                url_input = ''
            else:
                if ShortenURL.objects.filter(short_url=custom_short).exists():
                    custom_error = True
                else:
                    shortened_db.short_url = custom_short
                    try:
                        shortened_db.shortened_id = short.decode(custom_short)
                    except ValueError:
                        char_err = True
                    shortened_db.save()
                    shortened_url = request.build_absolute_uri(shortened_db.short_url)
                    url_input = ''


    # template = loader.get_template('URL_Shortner/index.html')
    # render to response should be updated for django versions
    return render(request, 'URL_Shortner/index.html', {'error': url_error, 'inv_err': char_err,
                                                       'cust_err': custom_error, 'url': url_input,
                                                       'short_url': shortened_url})


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def redirect_url(request, short):
    from user_agents import parse
    url_obj = get_object_or_404(ShortenURL, short_url=short)

    ShortenURL.objects.filter(short_url=short).update(hits=F('hits')+1)

    # if not URLVisits.objects.filter(url_id_fk=url_obj, visit_date=datetime.date.today()).exists():
    x = URLVisits()
    x.ip = get_client_ip(request)
    x.url_id_fk = url_obj
    x.os = parse(request.META.get('HTTP_USER_AGENT', '')).os.family
    print(parse(request.META.get('HTTP_USER_AGENT', '')))
    x.os = parse(request.META.get('HTTP_USER_AGENT', '')).browser.family
    x.os = parse(request.META.get('HTTP_USER_AGENT', '')).device.family
    # x.from_country =  # later
    # x.referral = 'Get referral web domain name'  # skip this for now
    x.save()
    return redirect(url_obj.url)


def stats(request, short):
    short_db = get_object_or_404(ShortenURL, short_url=short)

    stats = URLVisits.objects.filter(day__gt=datetime.date.today()-datetime.timedelta(days=30),
                                     url_id_fk=short_db).all()

    link_url = request.build_absolute_uri("/" + short_db.short_url)  # make it an absolute one

    # render to response should be updated for django versions
    return render_to_response("stats.html", {"stats": stats, "link": short_db, "link_url": link_url},
                              context_instance=RequestContext(request))


def custom_url(reuest):
    url, custom = reuest.POST.get('url', 'custom', '')
    short_obj = ShortUrl()
    short_id = short_obj.decode(custom)
    # if short_id not in DB
        # if url==VALID_URL:
        #     insert into DB
        #     return url
