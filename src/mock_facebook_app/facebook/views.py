import json
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.views import generic
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from django.http import HttpResponseRedirect, HttpResponse
from django.http import HttpResponseNotFound
from django.core.serializers.json import DjangoJSONEncoder

from facebook.models import Post, Like, Comment
from facebook.forms import LoginForm, SignUpForm, PostForm


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


class LoginUser(generic.TemplateView):
    template_name = "facebook/login-attempt.html"

    def get_context_data(self, **kwargs):
        error = ""
        if self.request.GET.get('login_error'):
            error = "Invalid username or password."

        context = {
            'loginform': LoginForm(),
            'error': error
        }
        return context


class HomeView(generic.TemplateView):
    template_name = "facebook/home.html"

    def get_context_data(self, **kwargs):
        posts = Post.objects.order_by('datetime').reverse()

        context = {
            'postform': PostForm(),
            'posts': posts,
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


class RemovePost(generic.View):

    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=request.POST['post-id'])

        if (post.user.id == request.user.id):
            post.delete()
            return HttpResponse(
                json.dumps({"success": True})
            )
        else:
            return HttpResponse(json.dumps({"success": False}))


class ToggleLike(generic.View):

    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=request.POST['post-id'])
        like = Like.objects.filter(user=request.user, post=post)

        if like:
            post.likes.filter(user=request.user).delete()
            s = self.countLikes(request.user, post)
            return HttpResponse(
                json.dumps({"innerHTML": "Like", "newCount": s})
            )
        else:
            like = Like(user=request.user, post=post)
            like.save()
            s = self.countLikes(request.user, post)
            return HttpResponse(
                json.dumps({"innerHTML": "Unlike", "newCount": s})
            )

    def countLikes(self, user, post):
        likes = Like.objects.filter(post=post)
        n = len(likes)
        s = ""

        if n == 0:
            s = 'Be the first one to like this post.'
        elif n == 1:
            if likes.last().user == user:
                s = "You like this."
            else:
                s = likes.last().user.first_name + " likes this."
        else:
            if likes.filter(user=user):
                name = "You"
            else:
                name = likes.last().user.first_name

            s = name + " and " + str(n - 1) + " other(s) like this."

        return s


class PostUpdate(generic.View):

    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=request.POST['post-id'])

        if post:
            data = {'text': post.text}
            html = render_to_string(
                "facebook/home_post_form.html",
                {"form": PostForm(initial=data),
                 "user": request.user,
                 "post": post}
            )

            return HttpResponse(html)
        else:
            return HttpResponse(json.dumps({"success": False}))


class EditPost(generic.View):

    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=request.POST['post-id'])

        if post:
            post.text = request.POST['text']
            post.save()
            html = render_to_string(
                "facebook/post.html", {"post": post, "user": request.user}
            )

            return HttpResponse(html)
        else:
            return HttpResponse(json.dumps({"success": False}))


def verifyLogin(request):

    user = authenticate(
        username=request.POST['username'],
        password=request.POST['password']
    )

    if user is not None:
        login(request, user)
    else:
        return HttpResponseRedirect(reverse('facebook:login')+"?login_error=1")

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
        if request.is_ajax():
            return HttpResponse('{"success": true}')
    else:
        s = "Error:\n"

        for keys in user_form.error_messages:
            s += user_form.error_messages[keys] + "\n"

        if request.is_ajax():
            return HttpResponse(
                json.dumps({"success": "false", "error": user_form.errors})
            )

    return HttpResponseRedirect(reverse('facebook:index'))


def post_status(request):

    p = Post(
        user=request.user,
        text=request.POST['text'],
        datetime=timezone.now())
    p.save()

    if request.is_ajax():
        html = render_to_string(
            "facebook/post.html", {"post": p, "user": request.user}
        )
        return HttpResponse(html)

    return HttpResponseRedirect(reverse('facebook:index'))


def logoutUser(request):
    logout(request)
    return HttpResponseRedirect(reverse('facebook:index'))
