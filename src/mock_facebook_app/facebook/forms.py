from django import forms
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.forms import UserCreationForm


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "username")


class PostForm(forms.Form):
    text = forms.CharField(
        widget=forms.Textarea(
            attrs={'placeholder': 'What\'s on your mind?'}
        )
    )
