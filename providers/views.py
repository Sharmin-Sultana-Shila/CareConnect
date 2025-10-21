from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from django.utils import timezone
from users.models import User, Booking
from .models import ServiceProvider, Task
from updates.models import Notification, EmergencySOS



# Create your views here.

def provider_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_provider:
            login(request, user)
            return redirect('provider_dashboard')

    return render(request, 'providers/login.html')
