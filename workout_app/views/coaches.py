from rest_framework.decorators import api_view
from rest_framework.response import Response
from workout_app.models import Coach
from workout_app.serializers.coach_serializer import CoachSerializer


@api_view(['GET'])
def get_all_coaches(_):
    coaches = Coach.objects.all()
    serializer = CoachSerializer(coaches, many=True)
    return Response(serializer.data)
