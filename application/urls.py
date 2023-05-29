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
    path('discover/', views.discover, name='discover'),
    path('profile/<int:id>/', views.profile_view, name='profile'),
    path('people', views.people_list, name='people'),
    path('follow/<int:pk>/', views.follow_user, name='follow_user'),
    path('like/<int:pk>/', views.like_post, name='like_post'),
    path('search/', views.search, name='search'),
    path('submit_comment/<int:post_pk>/', views.submit_comment, name='submit_comment'),
    path('my_likes/', views.my_likes, name='my_likes'),
]



