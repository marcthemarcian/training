from django.conf.urls import patterns, url
from facebook import views


urlpatterns = patterns(
    '',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^verifyLogin$', views.verifyLogin, name='verifyLogin'),
    url(r'^verifySignUp$', views.verifySignUp, name='verifySignUp'),
    url(r'^post_status$', views.post_status, name='post_status'),
    url(r'^logout$', views.logoutUser, name='logout')
)
