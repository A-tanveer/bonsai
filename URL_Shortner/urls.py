from django.conf.urls import url

from . import views

urlpatterns = [
    # url patterns should be more than 6 characters long
    url(r'^usersignup/$', views.signup, name='signup'),
    url(r'^usersignin/$', views.signin, name='signin'),
    url(r'^usersignout/$', views.log_out, name='logout'),
    # url(r'^statistics/$', views.stats, name='states'),
    url(r'^(?P<short>[a-zA-Z2-9-_]{1,6})$', views.redirect_url, name='redirectUrl'),
    url(r'^$', views.index, name='index'),
]
