from django.conf.urls import url

from . import views

urlpatterns = [
    # url patterns should be more than 6 characters long
    url(r'^shortened/$', views.shortened_form, name='shortened'),
    url(r'^makeshort/$', views.sorten_url, name='shorten'),
    url(r'^(?P<short>[a-zA-Z2-9-_]{1,6})$', views.redirect_url, name='redirectUrl'),
    url(r'^$', views.index, name='index'),
]
