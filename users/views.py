from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from datetime import datetime
from .models import User,Feedback,Booking




def home(request):
    return render(request, 'home.html')