from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password
import json

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
    if serializer.is_valid():
        sportsman = serializer.save()
        return Response({'message': 'Sportsman registered', 'id': sportsman.id}, status=status.HTTP_201_CREATED)
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
def login_view(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST method allowed'}, status=400)

    try:
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return JsonResponse({'error': 'Email and password are required'}, status=400)

        try:
            user = Sportsman.objects.get(email=email)
        except Sportsman.DoesNotExist:
            return JsonResponse({'error': 'Invalid email or password'}, status=400)

        if check_password(password, user.password):
            return JsonResponse({'id': user.id, 'name': user.name})
        else:
            return JsonResponse({'error': 'Invalid email or password'}, status=400)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)