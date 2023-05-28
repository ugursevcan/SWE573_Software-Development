
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Post, UserProfile, Comment, Location
from django.db import models
from django import forms
from django import forms
from .widgets import LocationWidget
from django import forms
from django.forms.widgets import TextInput
from django.utils.safestring import mark_safe


class LocationField(forms.CharField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widget = forms.TextInput(attrs={'class': 'form-control', 'id': 'location'})

class PostForm(forms.ModelForm):
    location = LocationField(required=False)

    class Meta:
        model = Post
        fields = ['title', 'content', 'image']

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