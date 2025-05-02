from rest_framework_simplejwt.authentication import JWTAuthentication
from workout_app.models import Sportsman


class SportsmanJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        try:
            user_id = validated_token.get("user_id")
            if user_id is None:
                return None
            return Sportsman.objects.get(id=user_id)
        except Sportsman.DoesNotExist:
            return None
