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
    

def user_signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        contactNo = request.POST.get('contactNo')
        address = request.POST.get('address')
        profile_image = request.FILES.get('profile_image')
        if password != password2:
            return redirect('user_signup')
        if User.objects.filter(username=username).exists():
            return redirect('user_signup')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            contactNo=contactNo,
            address=address,
            is_provider=False
        )
        if profile_image:
            user.profile_image = profile_image
            user.save()
        return redirect('user_login')

    return render(request, 'users/signup.html')
