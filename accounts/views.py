import requests
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.shortcuts import redirect, render

from .forms import UserLoginForm, UserRegistrationForm

User = get_user_model()

client_id = settings.GITHUB_CLIENT_ID
redirect_uri = 'http://localhost:8080/accounts/github/callback'
oauth_url = f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope=read:user"

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
        ctx = {
            'form': form,
            'oauth_github': oauth_url
        }
    return render(request, 'login.html', ctx)


def logout_view(request):
    logout(request)
    return redirect('index')

def github_callback_view(request):
    if request.method == 'GET':
        code = request.GET.get('code')
        client_id = settings.GITHUB_CLIENT_ID
        client_secret = settings.GITHUB_CLIENT_SECRET

        token_response = requests.post('https://github.com/login/oauth/access_token', data={
            'client_id': client_id,
            'client_secret': client_secret,
            'code': code
        }, headers={'Accept': 'application/json'})

        token_json = token_response.json()
        access_token = token_json.get('access_token')
        print('access_token: ', access_token)

        user_info_response = requests.get('https://api.github.com/user', headers={
            'Authorization': f'token {access_token}'
        })

        user_info = user_info_response.json()

        username = user_info.get('login')
        print('username: ', username)

        user, created = User.objects.get_or_create(username=username)

        login(request, user)

        return redirect('index')
