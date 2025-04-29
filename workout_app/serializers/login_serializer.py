from rest_framework import serializers
from workout_app.models import Sportsman
from django.contrib.auth.hashers import check_password


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        try:
            user = Sportsman.objects.get(email=email)
        except Sportsman.DoesNotExist:
            raise serializers.ValidationError('Invalid email or password')

        if not check_password(password, user.password):
            raise serializers.ValidationError('Invalid email or password')

        data['user'] = user
        return data
