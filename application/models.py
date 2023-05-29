from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.text import slugify




class Location(models.Model):
    name = models.CharField(max_length=255)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    bio = models.TextField(blank=True)
    followers = models.ManyToManyField("UserProfile", related_name='following', blank=True)

    def __str__(self):
        return f"{self.user.first_name}  {self.user.last_name}"

class Post(models.Model):
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to="uploads/", null=True, blank=True)
    content = models.TextField()
    link = models.CharField(max_length=500, null=True)
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True)
    #user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, blank=True)
    slug = models.SlugField(default="", null=False, blank=True, db_index=True)
    likers = models.ManyToManyField("UserProfile", related_name='liked_posts', blank=True)
    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True)
    memory_start_date = models.DateField(blank=True, null=True)
    memory_finish_date = models.DateField(blank=True, null=True)


    def get_absolute_url(self):
        return reverse("postDetailUrl", args=[self.slug])

    def __str__(self):
        return f"{self.title}  {self.author} {self.memory_start_date} {self.memory_finish_date}"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
