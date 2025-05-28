from django.db import models

from workout_app.models.sportsman import Sportsman


class MuscleGroup(models.Model):
    name = models.CharField(max_length=100)
    base_multiplier = models.FloatField(
        help_text="Multiplier relative to user body weight (e.g. 0.7 for chest)")

    def __str__(self):
        return str(self.name)


class BaseExercise(models.Model):
    name = models.CharField(max_length=255)
    muscle_group = models.ForeignKey(
        MuscleGroup, on_delete=models.SET_NULL, null=True)
    bodyweight = models.BooleanField(
        default=True, help_text="If true, uses body weight as resistance")
    notes = models.TextField(blank=True)

    def __str__(self):
        return str(self.name)


class CustomExercise(models.Model):
    user = models.ForeignKey(Sportsman, on_delete=models.CASCADE)
    program = models.ForeignKey(
        'UserProgram', on_delete=models.CASCADE, related_name='exercises'
    )
    base_exercise = models.ForeignKey(BaseExercise, on_delete=models.CASCADE)
    reps = models.PositiveIntegerField()
    sets = models.PositiveIntegerField()
    weight = models.FloatField(help_text="0 means bodyweight only.")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.name} - {self.base_exercise.name}"
