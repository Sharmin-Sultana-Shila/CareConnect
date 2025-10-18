from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from datetime import datetime
from providers.models import ServiceProvider,Task
from updates.models import Notification,EmergencySOS
from .models import User,Feedback,Booking




def home(request):
    return render(request, 'home.html')
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and not user.is_provider:
            login(request, user)
            return redirect('user_dashboard')
    return render(request, 'users/login.html')
