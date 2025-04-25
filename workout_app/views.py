from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
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
def registration(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        age = data.get('age')
        city_id = data.get('city')
        level_id = data.get('level')
        password = data.get('password')
        city = get_object_or_404(City, id=city_id)
        level = get_object_or_404(SportsmanLevel, id=level_id)

        sportsman = Sportsman.objects.create(
            name=name, age=age, city=city, level=level, password=password)
        return JsonResponse({'message': 'Sportsman registered', 'id': sportsman.id})
    return JsonResponse({'error': 'Invalid method'}, status=405)


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
