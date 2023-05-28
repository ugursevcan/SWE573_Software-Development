from django.contrib.auth import login
from .views import landing_page_view
from django.urls import include, path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', landing_page_view, name='landing'),
    path('register/', views.register, name='register'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('login/', views.login_view, name='login'),
    path('create_post/', views.create_post, name='create_post'),
    path('home/', views.home_view, name='home'),
    path('profile/<int:id>/', views.profile_view, name='profile'),
    path('follow/<int:pk>/', views.follow_user, name='follow_user'),
    path('like/<int:pk>/', views.like_post, name='like_post'),
    path('search/', views.search_view, name='search'),

]



