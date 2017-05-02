from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from URL_Shortner.models import ShortenURL, URLVisits
def index(request):
    c = {}
    c.update(cs)
    return HttpResponse("This is Shortner index")


def short_url(request, short):
    short_id = short_url.decode(short)
    url_obj = get_object_or_404(ShortenURL, shortened_id=short_id)
    url = url_obj.url
    str = "redirect to long url: " + short
    return HttpResponse(str)


def shortened_form(request):
    return HttpResponse("View shortened url")


class short_url():

    _alphabet = '23456789bcdfghjkmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ-_'
    _base = len(_alphabet)

    def encode(self, number):
        string = ''
        while(number > 0):
            string = self._alphabet[number % self._base] + string
            number //= self._base
        return string

    def decode(self, string):
        number = 0
        for char in string:
            number = number * self._base + self._alphabet.index(char)

        return number