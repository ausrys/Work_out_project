from django.db import models


class City(models.Model):
    city = models.CharField(max_length=100)

    def __str__(self):
        return str(self.city)


class SportsmanLevel(models.Model):
    level = models.CharField(max_length=100)

    def __str__(self):
        return str(self.level)


class Program(models.Model):
    date = models.DateField()
    name = models.CharField(max_length=200)
    program_description = models.TextField()
    levels = models.ForeignKey(
        SportsmanLevel, on_delete=models.SET_NULL, null=True, blank=True, related_name="programs")

    def __str__(self):
        return f"{self.name} ({self.date})"


class Sportsman(models.Model):
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    password = models.CharField(max_length=100)
    level = models.ForeignKey(
        SportsmanLevel, on_delete=models.SET_NULL, null=True, blank=True)
    city = models.ForeignKey(
        City, on_delete=models.SET_NULL, null=True, blank=True)
    program = models.ForeignKey(
        Program, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return str(self.name)
