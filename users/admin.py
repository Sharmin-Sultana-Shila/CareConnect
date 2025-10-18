from django.contrib import admin

from .models import User,Booking,Feedback
admin.site.register(User)
admin.site.register(Booking)
admin.site.register(Feedback)
# Register your models here.
