"""
URL configuration for careconnect project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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

from django.urls import path
from . import views
urlpatterns = [
    path('login/', views.user_login, name='user_login'),
    path('signup/', views.user_signup, name='user_signup'),
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('profile/', views.user_profile, name='user_profile'),
    path('logout/', views.user_logout, name='user_logout'),
    path('search/', views.search_providers, name='search_providers'),









]
