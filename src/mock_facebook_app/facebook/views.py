from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.views import generic
from django.contrib.auth.models import User
from facebook.forms import LoginForm
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse


class IndexView(generic.View):

    def dispatch(self, request, *args, **kwargs):
        handler_class = None

        if request.user.is_authenticated():
            handler_class = HomeView(request=request)
        else:
            handler_class = LoginView(request=request)

        if request.method.lower() in handler_class.http_method_names:
            handler = getattr(handler_class, request.method.lower(),
                              handler_class.http_method_not_allowed)
        else:
            handler = handler_class.http_method_not_allowed
        return handler(request, *args, **kwargs)


class LoginView(generic.TemplateView):
    template_name = "facebook/login.html"

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        context['form'] = LoginForm()
        return context


class HomeView(generic.TemplateView):
    template_name = "facebook/test.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        print self.request.user, "PLEASE PLEASE PLEASE"
        context = {
            'user': self.request.user
        }

        return context


def verifyLogin(request):
    user = authenticate(
        username=request.POST['username'],
        password=request.POST['password']
    )

    if user is not None:
        login(request, user)

    return HttpResponseRedirect(reverse('facebook:index'))


def logoutUser(request):
    logout(request)

    return HttpResponseRedirect(reverse('facebook:index'))
