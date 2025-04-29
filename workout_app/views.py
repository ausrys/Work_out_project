from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password
import json
from rest_framework_simplejwt.tokens import RefreshToken

from workout_app.serializers.login_serializer import LoginSerializer
from workout_app.serializers.programs_by_user_serializer import ProgramSerializer
from workout_app.serializers.sportsman_serializer import SportsmanRegisterSerializer
from .models import Program, Sportsman, SportsmanLevel, City

# Create your views here.


def program_list(request):
    programs = Program.objects.select_related('levels').all()
    result = []
    for p in programs:
        result.append({
            'id': p.id,
            'name': p.name,
            'date': p.date,
            'program_description': p.program_description,
            'level': p.levels.level if p.levels else None,
        })
    return JsonResponse(result, safe=False)


# 2. Register a sportsman
@csrf_exempt
@api_view(['POST'])
def registration(request):
    serializer = SportsmanRegisterSerializer(data=request.data)
    # If data is correct and fully provided, save new user
    if serializer.is_valid():
        sportsman = serializer.save()
        # Generate token
        refresh = RefreshToken.for_user(sportsman)
        return Response({
            'message': 'Sportsman registered',
            'id': sportsman.id,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def program_registration(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        level_id = data.get('level')
        program_description = data.get('program_description')
        date = data.get('date')
        level = get_object_or_404(SportsmanLevel, id=level_id)
        Program.objects.create(
            name=name, program_description=program_description, date=date, levels=level)
        return JsonResponse({'message': 'Program assigned'})
    return JsonResponse({'error': 'Invalid method'}, status=405)

# Login function


@csrf_exempt
@api_view(['POST'])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']

        # Generate tokens
        refresh = RefreshToken.for_user(user)

        return Response({
            'message': 'Login successful',
            'id': user.id,
            'name': user.name,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@permission_classes([IsAuthenticated])
def user_programs(request):
    # This will be your Sportsman instance (after small setup)
    user = request.user

    # Filter programs related to this Sportsman
    programs = Program.objects.filter(sportsman=user)

    serializer = ProgramSerializer(programs, many=True)
    return Response(serializer.data)
