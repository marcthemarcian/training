from django.shortcuts import get_object_or_404
from django.views import generic
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from facebook.models import Post, Like, Comment
from facebook.forms import LoginForm, SignUpForm, PostForm
from django.http import HttpResponseRedirect, HttpResponse
from django.http import HttpResponseNotFound


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
        posts = Post.objects.order_by('datetime').reverse()

        context = {
            'postform': PostForm(),
            'posts': posts
        }
        return context


class ProfileView(generic.DetailView):
    model = User
    template_name = "facebook/profile.html"

    def get_object(self, **kwargs):
        return get_object_or_404(User, username=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context['userprofile'] = self.object
        return context


def verifyLogin(request):

    user = authenticate(
        username=request.POST['username'],
        password=request.POST['password']
    )

    if user is not None:
        login(request, user)

    return HttpResponseRedirect(reverse('facebook:index'))


def verifySignUp(request):

    user_form = SignUpForm(request.POST)
    if user_form.is_valid():
        username = user_form.clean_username()
        password = user_form.clean_password2()
        user_form.save()
        user = authenticate(username=username,
                            password=password)
        login(request, user)
        return HttpResponseRedirect(reverse('facebook:index'))

    print user_form.error_messages
    return HttpResponse(user_form.error_messages['password_mismatch'])


def post_status(request):

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
