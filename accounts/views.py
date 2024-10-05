from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render

from .forms import UserLoginForm, UserRegistrationForm


def index(request):
    return render(request, 'index.html', {'user': request.user})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')  # Redirect to login page after registration
    else:
        form = UserRegistrationForm()
        client_id = settings.GITHUB_CLIENT_ID
        redirect_uri = 'http://localhost:8080/accounts/github/callback'
        oauth_url = f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope=read:user"
        ctx = {
            'form': form,
            'oauth_github': oauth_url
        }
    return render(request, 'register.html', ctx)

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')  # Redirect to home after login
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('index')

def github_oauth_view(request):
    if request.method == 'GET':
        code = request.GET.get('code')
        print('code: ', code)
        return redirect('index')

