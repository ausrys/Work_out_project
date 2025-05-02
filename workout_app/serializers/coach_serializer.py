from rest_framework import serializers
from workout_app.models import Coach

class CoachSerializer(serializers.ModelSerializer):
    city = serializers.StringRelatedField()

    class Meta:
        model = Coach
        fields = ['id', 'name', 'email', 'age', 'city', 'years_of_experience']
