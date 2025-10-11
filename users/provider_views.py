from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User, ServiceProvider


def provider_signup(request):
    """Provider Signup Page"""
    if request.method == 'POST':
        # User credentials
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        # Provider details
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

        # Validation
        if password != password2:
            messages.error(request, 'Passwords do not match!')
            return redirect('provider_signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
            return redirect('provider_signup')

        # Create User
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            contactNo=contactNo,
            address=location,
            is_provider=True
        )

        # Create ServiceProvider
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

        messages.success(request, 'Provider account created successfully! Please login.')
        return redirect('provider_login')

    return render(request, 'providers/signup.html')


def provider_login(request):
    """Provider Login Page"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_provider:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('provider_dashboard')
        else:
            messages.error(request, 'Invalid username/password or not a provider account!')

    return render(request, 'providers/login.html')