from django.db import models

from workout_app.models.utils import City


class Coach(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    age = models.PositiveIntegerField()
    city = models.ForeignKey(
        City, on_delete=models.SET_NULL, null=True, blank=True)
    years_of_experience = models.PositiveIntegerField()

    def __str__(self):
        return str(self.name)
