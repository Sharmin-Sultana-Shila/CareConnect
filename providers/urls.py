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
    path('login/', views.provider_login, name='provider_login'),
    path('signup/', views.provider_signup, name='provider_signup'),
    path('logout/', views.provider_logout, name='provider_logout'),
    path('dashboard/', views.provider_dashboard, name='provider_dashboard'),
    path('profile/', views.provider_profile, name='provider_profile'),
    path('bookings/', views.provider_bookings, name='provider_bookings'),
    path('tasks/', views.provider_tasks, name='provider_tasks'),
    path('task/complete/<int:task_id>/', views.complete_task, name='complete_task'),
    path('notifications/', views.provider_notifications, name='provider_notifications'),
    path('emergency/', views.send_emergency, name='send_emergency'),
    path('booking/accept/<int:booking_id>/', views.accept_booking, name='accept_booking'),

]
