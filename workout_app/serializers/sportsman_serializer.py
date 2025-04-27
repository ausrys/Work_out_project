from rest_framework import serializers
from workout_app.models import Sportsman
from django.contrib.auth.hashers import make_password

class SportsmanRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Sportsman
        fields = ['id', 'name', 'age', 'email', 'city', 'level', 'password']

    def validate_email(self, value):
        if Sportsman.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already registered")
        return value

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)
