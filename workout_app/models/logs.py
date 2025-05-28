from django.db import models
from django.utils import timezone

from workout_app.models.sportsman import Sportsman


class UserLog(models.Model):
    user = models.ForeignKey(Sportsman, on_delete=models.CASCADE)
    action = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.email} - {self.action} at {self.timestamp}"
