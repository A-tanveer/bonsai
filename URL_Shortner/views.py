import datetime

from django.contrib.auth import login, authenticate, logout
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.db.models import F
from django.shortcuts import get_object_or_404, render_to_response, redirect, render
from django.template import RequestContext

from .forms import SignUpForm
from .models import ShortenURL, URLVisits
from .short_url import ShortUrl


# use for user registration
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'URL_Shortner/signup.html', {'form': form})


# use for user sign in
def signin(request):
    login_err = False
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['passwd']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            login_err = True
    return render(request, 'URL_Shortner/signin.html', {'err': login_err})


def log_out(request):
    logout(request)
    return redirect('signin')


def index(request):
    url_error = False
    custom_error = False
    char_err = False
    url_input = ''
    shortened_url = ''
    custom_short = False

    if request.method == 'POST':
        validator = URLValidator()
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
            if not custom_short:
                shortened_url = request.build_absolute_uri(insert_Url(url_input))
                url_input = ''
            else:
                if ShortenURL.objects.filter(short_url__regex='^' + short + '$').exists():
                    custom_error = True
                else:
                    insert_custom(url_input, custom_short)
                    shortened_url = request.build_absolute_uri(custom_short)
                    url_input = ''
    return render(request, 'URL_Shortner/index.html', {'error': url_error, 'inv_err': char_err,
                                                      'cust_err': custom_error, 'url': url_input,
                                                      'short_url': shortened_url})


def insert_custom(url, short):
    """
    :param url: an valid url.
    :param short: an user prefered unique short code
    to do:  error checking should be done here. and raise exception.
    """
    urlDb = ShortenURL()
    urlDb.url = url
    urlDb.short_url = short
    urlDb.shortened_id = ShortUrl().decode(short)
    urlDb.save()


def insert_Url(url):
    """
    Takes an valid url or string as input, inserts it to database and returns an unique short code.
    :param url: valid url
    :return: short url
    """
    urlDb = ShortenURL()
    urlDb.url = url
    urlDb.save()
    short = ShortUrl().encode(urlDb.id)
    if ShortenURL.objects.filter(short_url__regex='^' + short + '$').exists():
        return insert_Url(url)
    urlDb.short_url = short
    urlDb.shortened_id = ShortUrl.decode(short)
    urlDb.save()
    return short


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def redirect_url(request, short):
    from user_agents import parse

    url_obj = get_object_or_404(ShortenURL, short_url__regex='^' + short + '$')

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
