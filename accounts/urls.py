from django.urls import path

from .views import github_callback_view, login_view, logout_view, register

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('github/callback', github_callback_view, name='github_oauth'),
]
