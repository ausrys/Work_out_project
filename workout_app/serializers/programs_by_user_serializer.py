from rest_framework import serializers
from workout_app.models import UserProgram, CustomExercise

class CustomExerciseSerializer(serializers.ModelSerializer):
    base_exercise_name = serializers.CharField(source='base_exercise.name')
    muscle_group = serializers.CharField(source='base_exercise.muscle_group.name')

    class Meta:
        model = CustomExercise
        fields = ['id', 'base_exercise_name', 'muscle_group', 'reps', 'sets', 'weight']

class UserProgramSerializer(serializers.ModelSerializer):
    exercises = CustomExerciseSerializer(many=True)

    class Meta:
        model = UserProgram
        fields = ['id', 'name', 'description', 'is_custom', 'created_at', 'exercises']
