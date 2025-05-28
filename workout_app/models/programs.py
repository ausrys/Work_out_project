from django.db import models

from workout_app.models.exercises import BaseExercise
from workout_app.models.sportsman import Sportsman


class UserProgram(models.Model):
    user = models.ForeignKey(Sportsman, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    is_custom = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name)


class BaseProgram(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    # True for free programs, False for premium
    created_at = models.DateTimeField(auto_now_add=True)
    exercises = models.ManyToManyField(
        BaseExercise, through='BaseProgramExercise', related_name='programs')

    def __str__(self):
        return str(self.name)


class BaseProgramExercise(models.Model):
    program = models.ForeignKey(BaseProgram, on_delete=models.CASCADE)
    exercise = models.ForeignKey(BaseExercise, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('program', 'exercise')

    def __str__(self):
        return f"{self.program.name} - {self.exercise.name}"
