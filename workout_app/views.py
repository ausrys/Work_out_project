from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt

from workout_app.auth.token_gen import get_tokens_for_user
from workout_app.serializers.coach_serializer import CoachSerializer
from workout_app.serializers.login_serializer import LoginSerializer
from workout_app.serializers.sportsman_serializer import SportsmanProfileSerializer,\
    SportsmanRegisterSerializer
from workout_app.serializers.programs_by_user_serializer import UserProgramSerializer
from .models import Coach, Sportsman, UserLog,  UserProgram

# Create your views here.


# 2. Register a sportsman
@csrf_exempt
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


@csrf_exempt
@api_view(['POST'])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        UserLog.objects.create(user=user, action="User logged in")
        tokens = get_tokens_for_user(user)
        return Response({
            'message': 'Login successful',
            'id': user.id,
            'name': user.name,
            'access': tokens['access'],
            'refresh': tokens['refresh']
        }, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def get_user_programs(request):
    user = request.user
    # Optional: Verify user is of type Sportsman if needed
    try:
        sportsman = Sportsman.objects.get(id=user.id)
    except Sportsman.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    programs = UserProgram.objects.filter(user=sportsman).prefetch_related('exercises__base_exercise__muscle_group')
    serializer = UserProgramSerializer(programs, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_user_profile(_, user_id):
    try:
        user = Sportsman.objects.get(id=user_id)
        serializer = SportsmanProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Sportsman.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_all_coaches(_):
    coaches = Coach.objects.all()
    serializer = CoachSerializer(coaches, many=True)
    return Response(serializer.data)
