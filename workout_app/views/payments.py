import os
import jwt
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, \
    authentication_classes
import stripe
from django.views.decorators.csrf import csrf_exempt
from workout_app.models import Sportsman, UserPayment


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
        success_url='http://localhost:5173/myprofile',
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
            UserPayment.objects.create(
                user=user,
                payment_value=10.00,  # Adjust dynamically if needed
            )
        except Sportsman.DoesNotExist:
            print(f"User with email {customer_email} not found.")

    return Response({'status': 'success'})
