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

def provider_signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        name = request.POST.get('name')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        location = request.POST.get('location')
        experience_year = request.POST.get('experience_year')
        skills = request.POST.get('skills')
        category = request.POST.get('category')
        contactNo = request.POST.get('contactNo')
        hourlyRate = request.POST.get('hourlyRate')
        profile_image = request.FILES.get('profile_image')

        if password != password2:
            return redirect('provider_signup')

        if User.objects.filter(username=username).exists():
            return redirect('provider_signup')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            contactNo=contactNo,
            address=location,
            is_provider=True
        )

        ServiceProvider.objects.create(
            user=user,
            name=name,
            age=age,
            gender=gender,
            location=location,
            experience_year=experience_year,
            skills=skills,
            category=category,
            contactNo=contactNo,
            hourlyRate=hourlyRate,
            profile_image=profile_image
        )
        return redirect('provider_login')

    return render(request, 'providers/signup.html')
