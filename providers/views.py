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

@login_required
def provider_dashboard(request):
    if not request.user.is_provider:
        return redirect('user_dashboard')
    provider = ServiceProvider.objects.get(user=request.user)
    total_bookings = Booking.objects.filter(provider=provider).count()
    completed_tasks = Task.objects.filter(provider=provider, status='completed').count()
    pending_tasks = Task.objects.filter(provider=provider, status__in=['assigned', 'in_progress']).count()

    context = {
        'provider': provider,
        'total_bookings': total_bookings,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
    }
    return render(request, 'providers/dashboard.html', context)


@login_required
def provider_profile(request):
    if not request.user.is_provider:
        return redirect('user_dashboard')

    provider = ServiceProvider.objects.get(user=request.user)

    if request.method == 'POST':
        provider.name = request.POST.get('name')
        provider.age = request.POST.get('age')
        provider.gender = request.POST.get('gender')
        provider.location = request.POST.get('location')
        provider.experience_year = request.POST.get('experience_year')
        provider.skills = request.POST.get('skills')
        provider.category = request.POST.get('category')
        provider.hourlyRate = request.POST.get('hourlyRate')
        provider.availability = request.POST.get('availability') == 'on'

        if request.FILES.get('profile_image'):
            provider.profile_image = request.FILES.get('profile_image')

        provider.save()
        return redirect('provider_dashboard')

    context = {'provider': provider}
    return render(request, 'providers/profile.html', context)


def provider_logout(request):

    logout(request)
    return redirect('home')

# provider er bookings gula
@login_required
def provider_bookings(request):
    if not request.user.is_provider:
        return redirect('user_dashboard')
    provider = ServiceProvider.objects.get(user=request.user)
    bookings = Booking.objects.filter(provider=provider).order_by('-created_at')
    context = {
        'provider': provider,
        'bookings': bookings,
    }
    return render(request, 'providers/bookings.html', context)

# provider er task gula
@login_required
def provider_tasks(request):
    if not request.user.is_provider:
        return redirect('user_dashboard')
    provider = ServiceProvider.objects.get(user=request.user)
    tasks = Task.objects.filter(provider=provider).order_by('-created_at')
    context = {
        'provider': provider,
        'tasks': tasks,
    }
    return render(request, 'providers/tasks.html', context)

@login_required
def complete_task(request, task_id):
    if not request.user.is_provider:
        return redirect('user_dashboard')
    provider = ServiceProvider.objects.get(user=request.user)
    task = get_object_or_404(Task, id=task_id, provider=provider)

    if request.method == 'POST':
        task.status = 'completed'
        task.completedAt = timezone.now()
        task.save()
        if task.booking:
            booking = task.booking
            all_tasks = booking.booking_tasks.all()
            all_completed = all(t.status == 'completed' for t in all_tasks)
            # jodi shobgula task complete hoye jay tkhn  status completed
            if all_completed:
                booking.status = 'completed'
                booking.save()
        Notification.objects.create(
            providerID=provider,
            userID=task.user,
            message=f"{provider.name} completed task: {task.description}",
            notification_type='task_completion'
        )
        return redirect('provider_tasks')

    context = {
        'provider': provider,
        'task': task,
    }
    return render(request, 'providers/complete_task.html', context)
@login_required
def provider_notifications(request):
    if not request.user.is_provider:
        return redirect('user_dashboard')
    provider = ServiceProvider.objects.get(user=request.user)
    notifications = Notification.objects.filter(userID=request.user).order_by('-time')
    notifications.update(isRead=True)

    context = {
        'provider': provider,
        'notifications': notifications,
    }
    return render(request, 'providers/notifications.html', context)


# emergency feature
@login_required
def send_emergency(request):
    if not request.user.is_provider:
        return redirect('user_dashboard')
    provider = ServiceProvider.objects.get(user=request.user)

    # provider jader kaj korse tader unique id gula nicche
    user_ids = Booking.objects.filter(provider=provider).values_list('user_id', flat=True).distinct()
    users = User.objects.filter(id__in=user_ids)
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        location = request.POST.get('location')
        description = request.POST.get('description')
        user = User.objects.get(id=user_id)
        EmergencySOS.objects.create(
            provider=provider,
            user=user,
            location=location,
            description=description
        )
        Notification.objects.create(
            providerID=provider,
            userID=user,

            notification_type='emergency'
        )
        return redirect('provider_dashboard')

    context = {
        'provider': provider,
        'users': users,
    }
    return render(request, 'providers/emergency.html', context)

@login_required
def accept_booking(request, booking_id):
    if not request.user.is_provider:
        return redirect('user_dashboard')
    provider = ServiceProvider.objects.get(user=request.user)
    booking = get_object_or_404(Booking, id=booking_id, provider=provider)

    if booking.status == 'pending':
        booking.status = 'confirmed'
        booking.save()

        Notification.objects.create(
            providerID=provider,
            userID=booking.user,
            message=f"{provider.name} accepted your booking #{booking.id}",
            notification_type='booking_accepted'
        )
    else:
        pass
    return redirect('provider_bookings')


