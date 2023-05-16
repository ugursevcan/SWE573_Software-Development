from django.contrib import admin
from .models import Post, Location
from .models import UserProfile

admin.site.register(Post)
admin.site.register(UserProfile)
admin.site.register(Location)

