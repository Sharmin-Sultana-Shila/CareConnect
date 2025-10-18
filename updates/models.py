from django.db import models
from users.models import User
from providers.models import ServiceProvider


class EmergencySOS(models.Model):
    provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE, related_name='sos_sent')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sos_received')
    location = models.CharField(max_length=300)
    description = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)

    def str(self):
        return f"EMERGENCY #{self.id} - {self.provider.name}"

    class Meta:
        db_table = 'updates_emergencysos'