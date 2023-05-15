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
from .models import UserProfile, User, Comment



def home_view(request):
    posts = Post.objects.all()
    return render(request, 'application/home.html', {'posts': posts})

def profile_view(request, id):
    profile = get_object_or_404(UserProfile, id=id)
    posts = Post.objects.filter(author=profile)

    return render(request, 'application/profile.html', {
        'profile': profile,
        #'is_following': profile.followers.contains(request.user.profile),
        "posts": posts,
        #"follower_count": profile.followers.count(),
        "profile_picture": profile.profile_picture
    })


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user.profile  # Access the UserProfile through the User object
            post.save()
            return redirect('home')
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
    user = request.user


    user_profile = request.user.profile
    print(user_profile)
    if target_profile.followers.contains(user_profile):
        target_profile.followers.remove(user_profile)
    else:
        target_profile.followers.add(user_profile)
    target_profile.save()
    print("Successfully added to followers")


    return HttpResponseRedirect('/user/' + str(user_to_follow.pk))
