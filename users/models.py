from django.db import models

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    contactNo = models.CharField(max_length=15)
    address = models.TextField()
    profile_image = models.ImageField(upload_to='user_profiles/', blank=True, null=True)
    is_provider = models.BooleanField(default=False)

    def __str__(self):
        return self.username

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_bookings')
    provider = models.ForeignKey('providers.ServiceProvider', on_delete=models.CASCADE, related_name='provider_bookings')
    dateTime = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    totalamount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking #{self.id}"

    class Meta:
        ordering = ['-created_at']


class Feedback(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='booking_feedback')
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback"