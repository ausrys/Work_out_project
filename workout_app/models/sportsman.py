from django.db import models

from workout_app.models.utils import City


class SportsmanLevel(models.Model):
    level = models.CharField(max_length=100)

    def __str__(self):
        return str(self.level)


class Sportsman(models.Model):
    SUBSCRIPTION_CHOICES = [
        ("free", "Free"),
        ("premium", "Premium"),
        ("pro", "Pro"),
    ]

    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    weight = models.PositiveIntegerField()
    gender = models.CharField(
        max_length=10, choices=GENDER_CHOICES)
    subscription_level = models.CharField(
        max_length=10, choices=SUBSCRIPTION_CHOICES, default='free')

    level = models.ForeignKey(
        SportsmanLevel, on_delete=models.SET_NULL, null=True, blank=True
    )
    city = models.ForeignKey(
        City, on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return str(self.name)
