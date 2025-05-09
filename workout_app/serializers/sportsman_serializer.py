from rest_framework import serializers
from django.contrib.auth.hashers import make_password

from workout_app.models import Sportsman


class SportsmanRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    weight = serializers.IntegerField(required=True)
    gender = serializers.ChoiceField(
        choices=[('male', 'Male'), ('female', 'Female')], required=True)

    class Meta:
        model = Sportsman
        fields = ['id', 'name', 'age', 'email', 'weight',
                  'gender', 'city', 'level', 'password']

    def validate_email(self, value):
        if Sportsman.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already registered")
        return value

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


class SportsmanProfileSerializer(serializers.ModelSerializer):
    city = serializers.StringRelatedField()
    level = serializers.StringRelatedField()

    class Meta:
        model = Sportsman
        exclude = ['password']  # exclude sensitive field
