from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Post
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Post, UserProfile, Comment
from django.db import models

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', "image"]

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
          'text': forms.Textarea(attrs={'rows':2}),
        }


class RegistrationForm(UserCreationForm):
    id = models.AutoField(primary_key=True)
    first_name = forms.CharField(max_length=101)
    last_name = forms.CharField(max_length=101)
    email = forms.EmailField()
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'profile_picture']