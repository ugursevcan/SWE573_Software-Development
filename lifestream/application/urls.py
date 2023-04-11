from django.contrib.auth import login
from django.urls import path
from .views import landing_page_view
from django.urls import include, path
from . import views
from django.contrib.auth.views import LoginView, LogoutView




urlpatterns = [
    path('', landing_page_view, name='landing'),
    path('register/', views.register, name='register'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('login/', views.login_view, name='login'),
]
