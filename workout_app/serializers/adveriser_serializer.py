from rest_framework import serializers
from django.contrib.auth.hashers import make_password, check_password
from workout_app.models import Advertiser, AdvertiserAPI


class AdvertiserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    weight = serializers.IntegerField(required=True)
    gender = serializers.ChoiceField(
        choices=[('male', 'Male'), ('female', 'Female')], required=True)

    class Meta:
        model = Advertiser
        fields = fields = ['email', 'password', 'company_name']

    def validate_email(self, value):
        if Advertiser.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "An account with this email already exists.")
        return value

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


class AdvertiserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        try:
            advertiser = Advertiser.objects.get(email=email)
        except Advertiser.DoesNotExist:
            raise serializers.ValidationError('Invalid email or password')

        if not check_password(password, advertiser.password):
            raise serializers.ValidationError('Invalid email or password')

        data['advertiser'] = advertiser
        return data


class AdvertiserAPISerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvertiserAPI
        fields = ['id', 'api_url', 'description', 'created_at']
        read_only_fields = ['id', 'created_at']
