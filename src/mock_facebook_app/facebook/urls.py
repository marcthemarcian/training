from django.conf.urls import patterns, url
from facebook import views


urlpatterns = patterns(
    '',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^verifyLogin$', views.verifyLogin, name='verifyLogin'),
    url(r'^logout$', views.logoutUser, name='logout')
)
