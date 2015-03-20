from django import forms
from django.contrib.auth.models import User
from django.db import models


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)


class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')
        widgets = {
            'password': forms.PasswordInput
        }


class PostForm(forms.Form):
    text = forms.CharField(
        widget=forms.Textarea(
            attrs={'placeholder': 'What\'s on your mind?'}
        )
    )
