from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from workout_app.auth.token_gen import get_tokens_for_user
from workout_app.models import UserLog
from workout_app.serializers.login_serializer import LoginSerializer
from workout_app.serializers.sportsman_serializer import \
    SportsmanRegisterSerializer
# Register a sportsman


@api_view(['POST'])
def registration(request):
    serializer = SportsmanRegisterSerializer(data=request.data)
    # If data is correct and fully provided, save new user
    if serializer.is_valid():
        sportsman = serializer.save()
        return Response({
            'message': 'Sportsman registered',
            'id': sportsman.id,
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Login function


@api_view(['POST'])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        UserLog.objects.create(user=user, action="User logged in")
        token = get_tokens_for_user(user)
        response = Response(status=status.HTTP_200_OK)
        response.set_cookie(key="auth_token", value=token, httponly=True)
        return response

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
