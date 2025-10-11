from django.shortcuts import render

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .models import User


def home(request):
    return render(request, 'home.html')


def user_signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        contactNo = request.POST.get('contactNo')
        address = request.POST.get('address')

        if password != password2:
            messages.error(request, 'Passwords do not match!')
            return redirect('user_signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
            return redirect('user_signup')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            contactNo=contactNo,
            address=address,
            is_provider=False
        )

        messages.success(request, 'Account created successfully! Please login.')
        return redirect('user_login')

    return render(request, 'users/signup.html')

# Create your views here.
