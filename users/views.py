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


@login_required
def user_dashboard(request):
    if request.user.is_provider:
        return redirect('provider_dashboard')
    return render(request, 'users/dashboard.html')


@login_required
def user_profile(request):
    if request.user.is_provider:
        return redirect('provider_dashboard')
    if request.method == 'POST':
        request.user.username = request.POST.get('username')
        request.user.email = request.POST.get('email')
        request.user.contactNo = request.POST.get('contactNo')
        request.user.address = request.POST.get('address')

        if request.FILES.get('profile_image'):
            request.user.profile_image = request.FILES.get('profile_image')
        request.user.save()
        return redirect('user_dashboard')
    return render(request, 'users/profile.html')
    
def user_logout(request):
    logout(request)
    return redirect('home')

# provider ke search kortese

@login_required
def search_providers(request):
    category = request.GET.get('category', '')
    location = request.GET.get('location', '')

    providers = ServiceProvider.objects.all()

    # category onushare filter
    if category:
        providers = providers.filter(category=category)

    # location onushare filter
    if location:
        providers = providers.filter(location__icontains=location)

    context = {
        'providers': providers,
        'category': category,
        'location': location,
    }
    return render(request, 'users/search.html', context)

@login_required
def provider_detail(request, pk):
    provider = ServiceProvider.objects.get(pk=pk)
    # booking__provider = booked provider db theke ami jake khujtesi tar shathe match koro
    # order_by= amon vabe sort koro jeno
    # -created_at = minus(-) bolte decensing order
    # [:5] = prothom 5 ta slice
    # orthat most recent 5 ta feedback dekhaw
    feedbacks = Feedback.objects.filter(booking__provider=provider).order_by('-created_at')[:5]

    # rating calculation hoitese
    context = {
        'provider': provider,
        'feedbacks': feedbacks,
    }
    return render(request, 'users/provider_detail.html', context)

# provider ke book korbe
@login_required
def book_provider(request, pk):

    provider = ServiceProvider.objects.get(pk=pk)

    if request.method == 'POST':
        dateTime_str = request.POST.get('dateTime')
        selected_tasks = request.POST.getlist('tasks')
        dateTime = datetime.strptime(dateTime_str, '%Y-%m-%dT%H:%M')

        totalamount = len(selected_tasks) * provider.hourlyRate
        booking = Booking.objects.create(
            user=request.user,
            provider=provider,
            dateTime=dateTime,
            totalamount=totalamount,
            status='pending'
        )

        for task_desc in selected_tasks:
            Task.objects.create(
                provider=provider,
                user=request.user,
                booking=booking,
                description=task_desc,
                status='assigned'
            )

        Notification.objects.create(
            providerID=provider,
            userID=provider.user,
            message=f"New booking from {request.user.username} for {dateTime.strftime('%Y-%m-%d %H:%M')}",
            notification_type='booking'
        )
        return redirect('user_bookings')

    context = {
        'provider': provider,
    }
    return render(request, 'users/book_provider.html', context)

@login_required
def delete_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    booking.booking_tasks.all().delete()
    booking.delete()
    return redirect('user_bookings')

@login_required
def user_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'bookings': bookings,
    }
    return render(request, 'users/bookings.html', context)
    
@login_required
def edit_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if request.method == 'POST':
        dateTime_str = request.POST.get('dateTime')

        if dateTime_str:
            from datetime import datetime
            try:
                dateTime = datetime.strptime(dateTime_str, '%Y-%m-%dT%H:%M')
                booking.dateTime = dateTime
                booking.save()
                return redirect('user_bookings')
            except ValueError:
                pass

    context = {
        'booking': booking,
    }
    return render(request, 'users/edit_booking.html', context)

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    if request.method == 'POST':
        booking.status = 'cancelled'
        booking.save()
        Notification.objects.create(
            providerID=booking.provider,
            userID=booking.provider.user,
            message=f"{request.user.username} cancelled booking #{booking.id}",
            notification_type='cancellation'
        )
        return redirect('user_bookings')

    context = {
        'booking': booking,
    }
    return render(request, 'users/cancel_booking.html', context)

@login_required
def user_notifications(request):
    if request.user.is_provider:
        return redirect('provider_dashboard')
    notifications = Notification.objects.filter(userID=request.user).order_by('-time')
    notifications.update(isRead=True)

    context = {
        'notifications': notifications,
    }
    return render(request, 'users/notifications.html', context)


@login_required
def emergency_alerts(request):
    if request.user.is_provider:
        return redirect('provider_dashboard')
    alerts = EmergencySOS.objects.filter(user=request.user).order_by('-time')

    context = {
        'alerts': alerts,
    }
    return render(request, 'users/emergency_alerts.html', context)

@login_required
def add_feedback(request, booking_id):
    # booking = Booking.objects.get(id=booking_id) dei nai karon je kew amr booking access korte parbe
    # tai security purpose e amr booking jate ami access korte pari, onno kew korte gele 404 error dibe

    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if request.method == 'POST':
        comment = request.POST.get('comment')

        Feedback.objects.create(
            booking=booking,
            comment=comment
        )


        Notification.objects.create(
            providerID=booking.provider,
            userID=booking.provider.user,
            message=f"{request.user.username} left a review",
            notification_type='review'
        )
        return redirect('user_bookings')

    context = {
        'booking': booking,
    }
    return render(request, 'users/add_feedback.html', context)



