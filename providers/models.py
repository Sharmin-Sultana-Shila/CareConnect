from django.db import models

from users.models import User


class ServiceProvider(models.Model):
    CATEGORY_CHOICES = [
        ('maid', 'House Maid'),
        ('babysitter', 'Babysitter'),
        ('caregiver', 'Caregiver'),
    ]

    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='provider_profile')
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    location = models.CharField(max_length=200)
    experience_year = models.FloatField()
    skills = models.TextField(help_text="Comma-separated")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    contactNo = models.CharField(max_length=15)
    hourlyRate = models.FloatField()
    availability = models.BooleanField(default=True)
    profile_image = models.ImageField(upload_to='provider_profiles/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.get_category_display()}"

    def get_skills_list(self):
        return [skill.strip() for skill in self.skills.split(',')]

class Task(models.Model):

    STATUS_CHOICES = [
        ('assigned', 'Assigned'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE, related_name='provider_tasks')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_tasks')
    booking = models.ForeignKey('users.Booking', on_delete=models.CASCADE, related_name='booking_tasks', null=True,
                                blank=True)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='assigned')
    completedAt = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Task #{self.id}"

    class Meta:
        ordering = ['-created_at']

