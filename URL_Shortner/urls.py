from django.conf.urls import url

from . import views

urlpatterns = [
    # url patterns should be more than 6 characters long
    url(r'^(?P<sign_in_or_up>(usersignin|createnewuser))/$', views.UserFormView.as_view(), name='login'),
    url(r'^statistics/$', views.stats, name='states'),
    url(r'^(?P<short>[a-zA-Z2-9-_]{1,6})$', views.redirect_url, name='redirectUrl'),
    url(r'^$', views.index, name='index'),
]
