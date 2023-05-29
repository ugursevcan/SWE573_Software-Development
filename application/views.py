from django.http import HttpResponseRedirect
from .forms import RegistrationForm, CommentForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import PostForm
from .models import UserProfile, User, Comment, Location, Post
from django.contrib.auth.models import User
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance

from django.db.models import Q
from datetime import datetime
from django.utils import timezone


def search(request):
    query = request.GET.get('query')
    latitude = request.GET.get('latitude')
    longitude = request.GET.get('longitude')
    search_start_date = request.GET.get('search_start_date')
    search_end_date = request.GET.get('search_end_date')

    print(f"Search Parameters: {query}, {latitude}, {longitude}, {search_start_date}, {search_end_date}")

    posts = Post.objects.none()

    if query:
        posts = Post.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))
        print(f"Posts after keyword search: {posts}")

    if latitude and longitude:
        latitude = float(latitude)
        longitude = float(longitude)

        location_posts = Post.objects.filter(
            location__latitude__range=(latitude - 1, latitude + 1),
            location__longitude__range=(longitude - 1, longitude + 1)
        )
        posts = posts | location_posts
        print(f"Posts after location search: {posts}")

    if search_start_date and search_end_date:
        # Convert string dates to date objects
        start_date = timezone.datetime.strptime(search_start_date, '%Y-%m-%d').date()
        end_date = timezone.datetime.strptime(search_end_date, '%Y-%m-%d').date()

        print(f"Search Dates: Start-{start_date}, End-{end_date}")

        # Filter for posts where the memory_start_date is before the search end date and the memory_finish_date is after the search start date
        posts = posts.filter(memory_start_date__lte=end_date, memory_finish_date__gte=start_date)
        print(f"Posts after date search: {posts}")

    posts = posts.order_by('date_created')
    return render(request, 'application/search.html', {'posts': posts})


def home_view(request):
    posts = Post.objects.all()
    comment_form = CommentForm()

    for post in posts:
        print(post.id)
        print(post.image.url)

    return render(request, 'application/home.html', {"posts": posts, "comment_form": comment_form})

def profile_view(request, id):
    profile = get_object_or_404(UserProfile, id=id)



    is_following = profile.followers.filter(id=request.user.profile.id).exists()

    return render(request, 'application/profile.html', {
        'profile': profile,
        'is_following': is_following,
        "posts": Post.objects.filter(Q(author=profile)),
        'follower_count': profile.followers.count(),
        'profile_picture': profile.profile_picture
    })



@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            location_name = form.cleaned_data.get('location')
            latitude = request.POST.get('latitude')
            longitude = request.POST.get('longitude')
            print(latitude)

            location, _ = Location.objects.get_or_create(
                name=location_name,
                latitude=latitude,
                longitude=longitude,
            )
            post = form.save(commit=False)
            post.location = location
            post.author = request.user.profile
            post.memory_start_date = timezone.datetime.strptime(request.POST.get('memory_start_date'), '%Y-%m-%d').date()
            post.memory_finish_date = timezone.datetime.strptime(request.POST.get('memory_finish_date'), '%Y-%m-%d').date()
            print(type(post.memory_start_date))
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
def discover(request):
    posts = Post.objects.all().order_by('-date_created')  # Retrieve all posts, ordered by the most recent first
    return render(request, 'application/discover.html', {'posts': posts})

@login_required
def my_likes(request):
    posts = Post.objects.all().order_by('-date_created')  # Retrieve all posts, ordered by the most recent first
    return render(request, 'application/my_likes.html', {'posts': posts})

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


@login_required
def people_list(request):
    profiles = UserProfile.objects.all()
    return render(request, 'application/people.html', {'profiles': profiles})

@login_required
def submit_comment(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    form = CommentForm(request.POST, request.FILES)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user  # assign the current user to the comment
        comment.post = post
        comment.save()
    return redirect(request.META.get('HTTP_REFERER'))

