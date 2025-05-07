from django.db import models
from django.utils import timezone


class City(models.Model):
    city = models.CharField(max_length=100)

    def __str__(self):
        return str(self.city)


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


class Coach(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    age = models.PositiveIntegerField()
    city = models.ForeignKey(
        City, on_delete=models.SET_NULL, null=True, blank=True)
    years_of_experience = models.PositiveIntegerField()

    def __str__(self):
        return str(self.name)


class UserLog(models.Model):
    user = models.ForeignKey(Sportsman, on_delete=models.CASCADE)
    action = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.email} - {self.action} at {self.timestamp}"


class UserPayment(models.Model):

    user = models.ForeignKey('Sportsman', on_delete=models.CASCADE)
    payment_value = models.DecimalField(max_digits=10, decimal_places=2)
    date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.payment_value} USD"
