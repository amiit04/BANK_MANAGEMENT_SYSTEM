"""
URL configuration for banking project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import home, handleSignup, handleLogin, handleLogout, profile, transfer, about, history, update

urlpatterns = [
    path('', home, name = 'home'),
    path('signup', handleSignup, name = 'signup'),
    path('login', handleLogin, name = 'login'),
    path('logout', handleLogout, name = 'logout'),
    path('profile', profile, name = 'profile'),
    path('transfer', transfer, name = 'transfer'),
    path('about', about, name = 'about'),
    path('history', history, name = 'history'),
    path('update', update, name = 'update'),
]
