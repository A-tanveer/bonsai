import datetime

from django.contrib.auth import login
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.db.models import F
from django.shortcuts import get_object_or_404, render_to_response, redirect, render
from django.template import RequestContext
from django.views.generic import View

from .forms import UserForm
from .models import ShortenURL, URLVisits
from .short_url import ShortUrl


class UserFormView(View):
    form_class = UserForm
    template = 'URL_Shortner/signin.html'

    # display blank form
    def get(self, request, sign_in_or_up):
        form = self.form_class(None)
        return render(request, self.template, {'form': form,
                                               'val': sign_in_or_up})

    # process data
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():

            user = form.save(commit=False)

            username = form.cleaned_data['usename']
            password = form.cleaned_data['password']
            user.username = username
            user.set_password(password)
            user.save()

            if user is not None:

                if user.is_active:
                    login(request, user)
                    return redirect('URL_Shortner:index')

        return render(request, self.template, {'form': form})


# from django.contrib.gis.geoip import GeoIP
def user_reg(request, sign_in_or_up):
    sign_val = sign_in_or_up

    username, password = None, None
    email = None
    first_name, last_name = None, None
    if request.method == 'POST':
        pass
    return render(request, 'URL_Shortner/signin.html', {'val': sign_in_or_up})


def index(request):
    url_error = False
    custom_error = False
    char_err = False
    url_input = ''
    shortened_url = ''
    custom_short = False

    if request.method == 'POST':
        validator = URLValidator()
        # here presence of a second argument should be checked. if present this thing will be different
        try:
            url_input = request.POST.get('url', None)
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
    return render(request, 'URL_Shortner/home.html', {'error': url_error, 'inv_err': char_err,
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

    ShortenURL.objects.filter(short_url=short).update(hits=F('hits') + 1)

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

    stats = URLVisits.objects.filter(day__gt=datetime.date.today() - datetime.timedelta(days=30),
                                     url_id_fk=short_db).all()

    link_url = request.build_absolute_uri("/" + short_db.short_url)  # make it an absolute one

    # render to response should be updated for django versions
    return render_to_response("stats.html", {"stats": stats, "link": short_db, "link_url": link_url},
                              context_instance=RequestContext(request))
