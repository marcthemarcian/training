from django.conf.urls import patterns, url

from facebook import views


urlpatterns = patterns(
    '',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^verifyLogin$', views.VerifyLogin.as_view(), name='verifyLogin'),
    url(r'^verifySignUp$', views.VerifySignUp.as_view(), name='verifySignUp'),
    url(r'^login$', views.LoginUser.as_view(), name='login'),
    url(r'^post_status$', views.PostStatus.as_view(), name='post_status'),
    url(r'^remove_post$', views.RemovePost.as_view(), name='remove_post'),
    url(r'^update_post$', views.PostUpdate.as_view(), name='update_post'),
    url(r'^submit_editForm$',
        views.EditPost.as_view(),
        name='submit_editForm'),
    url(r'^toggle_like$', views.ToggleLike.as_view(), name='toggle_like'),
    url(r'^logout$', views.LogoutUser.as_view(), name='logout'),
    url(r'^(?P<slug>[\w@+._-]+)$', views.ProfileView.as_view(), name='profile')
)
