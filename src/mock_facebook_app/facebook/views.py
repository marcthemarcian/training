from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from facebook.models import Post, Like, Comment
from facebook.forms import LoginForm, SignUpForm, PostForm
from django.utils import timezone


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
        context = {
            'loginform': LoginForm(),
            'signupform': SignUpForm()
        }
        return context


class HomeView(generic.TemplateView):
    template_name = "facebook/home.html"

    def get_context_data(self, **kwargs):
        print self.request, "hahaha"
        posts = Post.objects.order_by('datetime').reverse()

        context = {
            'postform': PostForm(),
            'posts': posts
        }
        return context


def verifyLogin(request):
    if 'HTTP_REFERRER' in request:
      print "blah"
    else:
      print "boo"

    user = authenticate(
        username=request.POST['username'],
        password=request.POST['password']
    )

    if user is not None:
        login(request, user)

    return HttpResponseRedirect(reverse('facebook:index'))


def verifySignUp(request):
    user = User(
        username=request.POST['username'],
        first_name=request.POST['first_name'],
        last_name=request.POST['last_name'],
        email=request.POST['email'],
    )
    user.set_password(request.POST['password'])
    user.save()
    return HttpResponseRedirect(reverse('facebook:index'))


def post_status(request):
    print request, "hihihi"
    if request.POST['text'] != "":
        p = Post(
            user=request.user,
            text=request.POST['text'],
            datetime=timezone.now())
        p.save()

    return HttpResponseRedirect(reverse('facebook:index'))


def logoutUser(request):
    logout(request)

    return HttpResponseRedirect(reverse('facebook:index'))
