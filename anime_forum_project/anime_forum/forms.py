from django import forms
from .models import Thread, Post
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class ThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ['category', 'title', 'content']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']


User = get_user_model()


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
