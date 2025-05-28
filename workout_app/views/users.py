from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.shortcuts import redirect
from workout_app.auth.user_auth import is_user_authenticated
from workout_app.models import Sportsman, UserPayment, UserProgram
from workout_app.serializers.payments_serializer import UserPaymentSerializer
from workout_app.serializers.programs_by_user_serializer \
    import UserProgramSerializer
from workout_app.serializers.sportsman_serializer import \
    SportsmanProfileSerializer


@api_view(['GET'])
def get_user_profile(request):
    token = request.COOKIES.get("auth_token")
    payload = is_user_authenticated(token)

    if not payload:
        return Response({'error': 'Unauthenticated action, please log in'},
                        status=status.HTTP_401_UNAUTHORIZED)
    try:
        user = Sportsman.objects.get(id=payload['id'])
        serializer = SportsmanProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Sportsman.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_user_programs(request):
    token = request.COOKIES.get("auth_token")
    payload = is_user_authenticated(token)
    try:
        sportsman = Sportsman.objects.get(id=payload['id'])
    except Sportsman.DoesNotExist:
        return Response({'error': 'User not found'},
                        status=status.HTTP_404_NOT_FOUND)

    programs = UserProgram.objects.filter(user=sportsman).prefetch_related(
        'exercises__base_exercise__muscle_group')
    serializer = UserProgramSerializer(programs, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def user_payments(request):
    token = request.COOKIES.get("auth_token")
    payload = is_user_authenticated(token)
    user = Sportsman.objects.get(id=payload['id'])
    payments = UserPayment.objects.filter(
        user=user).order_by('-date_time')
    serializer = UserPaymentSerializer(payments, many=True)
    return Response(serializer.data)
