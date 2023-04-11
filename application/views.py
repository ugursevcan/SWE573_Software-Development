from django.shortcuts import render
from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm

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
    return render(request, 'application/base.html')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/') # replace with the URL name of your base page
    else:
        form = RegistrationForm()
    return render(request, 'application/register.html', {'form': form})