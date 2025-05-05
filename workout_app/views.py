import os

import stripe
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, \
    authentication_classes
from django.views.decorators.csrf import csrf_exempt
import jwt
from workout_app.auth.token_gen import get_tokens_for_user

from workout_app.serializers.coach_serializer import CoachSerializer
from workout_app.serializers.login_serializer import LoginSerializer
from workout_app.serializers.sportsman_serializer import\
    SportsmanProfileSerializer, SportsmanRegisterSerializer
from workout_app.serializers.programs_by_user_serializer import\
    UserProgramSerializer
from .models import Coach, Sportsman, UserLog,  UserProgram

# Create your views here.


# 2. Register a sportsman
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


@api_view(['GET'])
def get_user_programs(request):
    token = request.COOKIES.get("auth_token")
    if not token:
        return Response({'error': 'Unauthenticated, please log in'},
                        status=status.HTTP_400_BAD_REQUEST)
    # Optional: Verify user is of type Sportsman if needed
    try:
        payload = jwt.decode(
            token, key=os.environ['JWTSECRET'], algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return Response({'error': 'Unauthenticated, please log in'},
                        status=status.HTTP_400_BAD_REQUEST)
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
def get_user_profile(request):
    token = request.COOKIES.get("auth_token")
    if not token:
        return Response({'error': 'Unauthenticated, please log in'},
                        status=status.HTTP_400_BAD_REQUEST)
    try:
        payload = jwt.decode(
            token, key=os.environ['JWTSECRET'], algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return Response({'error': 'Unauthenticated, please log in'},
                        status=status.HTTP_400_BAD_REQUEST)
    try:
        user = Sportsman.objects.get(id=payload['id'])
        serializer = SportsmanProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Sportsman.DoesNotExist:
        return Response({'error': 'User not found'},
                        status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_all_coaches(_):
    coaches = Coach.objects.all()
    serializer = CoachSerializer(coaches, many=True)
    return Response(serializer.data)


STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY')
STRIPE_PUBLIC_KEY = os.getenv('STRIPE_PUBLIC_KEY')
stripe.api_key = STRIPE_SECRET_KEY
endpoint_secret = os.getenv('STRIPE_WEBHOOK_SECRET')


@api_view(['POST'])
def create_checkout_session(request):
    token = request.COOKIES.get("auth_token")
    if not token:
        return Response({'error': 'Unauthenticated, please log in'},
                        status=status.HTTP_400_BAD_REQUEST)
    try:
        payload = jwt.decode(
            token, key=os.environ['JWTSECRET'], algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return Response({'error': 'Unauthenticated, please log in'},
                        status=status.HTTP_400_BAD_REQUEST)
    try:
        user = Sportsman.objects.get(id=payload['id'])
    except Sportsman.DoesNotExist:
        return Response({'error': 'User not found'},
                        status=status.HTTP_404_NOT_FOUND)
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        customer_email=user.email,
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': 'Premium Program Access',
                },
                'unit_amount': 1000,  # $10.00
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url='http://localhost:5173/success',
        cancel_url='http://localhost:5173/cancel',
    )
    return Response({'id': session.id})


@api_view(['POST'])
@authentication_classes([])  # Disable authentication for the webhook
@permission_classes([])      # Disable permission checks for the webhook
@csrf_exempt                 # CSRF exemption is required for webhooks
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError:
        return Response({'error': 'Invalid payload'}, status=status.HTTP_400_BAD_REQUEST)
    except stripe.error.SignatureVerificationError:
        return Response({'error': 'Invalid signature'}, status=status.HTTP_400_BAD_REQUEST)

    # Handle the checkout session completion
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        customer_email = session.get('customer_email')

        try:
            # Upgrade user tier
            user = Sportsman.objects.get(email=customer_email)
            user.subscription_level = 'premium'
            user.save()
            print(f"User {user.email} upgraded to premium.")
        except Sportsman.DoesNotExist:
            print(f"User with email {customer_email} not found.")

    return Response({'status': 'success'})
