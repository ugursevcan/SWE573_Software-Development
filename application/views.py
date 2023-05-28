from django.http import HttpResponseRedirect
from .forms import RegistrationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import PostForm
from .models import Post
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .models import UserProfile, User, Comment, Location
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User

from django.shortcuts import render
from .models import Post
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from .models import Post


def search_view(request):
    query_title = request.GET.get('title')
    query_content = request.GET.get('content')
    query_location = request.GET.get('location')
    query_radius = request.GET.get('radius')

    if query_title or query_content or (query_location and query_radius):
        posts = Post.objects.all()
        if query_title:
            posts = posts.filter(title__icontains=query_title)
        if query_content:
            posts = posts.filter(content__icontains=query_content)
        if query_location and query_radius:
            query_location = Point(query_location)
            posts = posts.filter(location__distance_lte=(query_location, query_radius))
    else:
        posts = Post.objects.none()

    return render(request, 'application/search.html', {'posts': posts})

def home_view(request):
    posts = Post.objects.all()

    for post in posts:
        print(post.id)
        print(post.image.url)


    return render(request, 'application/home.html', {'posts': posts})

def profile_view(request, id):
    profile = get_object_or_404(UserProfile, id=id)
    posts = Post.objects.filter(author=profile)

    is_following = profile.followers.filter(id=request.user.profile.id).exists()

    return render(request, 'application/profile.html', {
        'profile': profile,
        'is_following': is_following,
        'posts': posts,
        'follower_count': profile.followers.count(),
        'profile_picture': profile.profile_picture
    })



@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            location_name = form.cleaned_data.get('location')
            latitude = form.cleaned_data.get('latitude')
            longitude = form.cleaned_data.get('longitude')
            location, _ = Location.objects.get_or_create(
                name=location_name,
                defaults={'latitude': latitude, 'longitude': longitude},
            )
            post = form.save(commit=False)
            post.location = location
            post.save()
            return redirect('home')
        else:
            print(form.errors)
    else:
        form = PostForm()
    return render(request, 'application/create_post.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/') # replace with the URL name of your base page
        else:
            # handle invalid login
            pass
    return render(request, 'application/login.html')
def landing_page_view(request):
    return render(request, 'application/landing.html')




def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()

            # Create a user profile for the registered user
            UserProfile.objects.create(user=user, profile_picture=form.cleaned_data['profile_picture'])

            # Login the user after registration
            user = authenticate(username=user.username, password=form.cleaned_data['password1'])
            login(request, user)

            return redirect('/')  # Replace with the URL name of your base page
    else:
        form = RegistrationForm()
    return render(request, 'application/register.html', {'form': form})


@login_required
def home_view(request):
    posts = Post.objects.all().order_by('-date_created')  # Retrieve all posts, ordered by the most recent first
    return render(request, 'application/home.html', {'posts': posts})

@login_required
def follow_user(request, pk):
    # Get the user that the logged-in user wants to follow
    user_to_follow = get_object_or_404(User, pk=pk)
    target_profile = user_to_follow.profile
    user_profile = request.user.profile

    if target_profile.followers.filter(id=user_profile.id).exists():
        target_profile.followers.remove(user_profile)
    else:
        target_profile.followers.add(user_profile)

    return HttpResponseRedirect('/profile/' + str(user_to_follow.pk))


@login_required
def like_post(request, pk):
    post_to_like = get_object_or_404(Post, pk=pk)
    user_profile = request.user.profile

    if post_to_like.likers.filter(pk=user_profile.pk).exists():
        post_to_like.likers.remove(user_profile)
    else:
        post_to_like.likers.add(user_profile)

    return redirect(request.META.get('HTTP_REFERER'))
