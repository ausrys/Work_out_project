from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django.core.cache import cache
from workout_app.auth.token_gen import get_tokens_for_user
from workout_app.auth.user_auth import is_user_authenticated
from workout_app.models import Advertiser
from workout_app.serializers.adveriser_serializer import \
    AdvertiserAPISerializer, AdvertiserLoginSerializer, \
    AdvertiserRegisterSerializer


@api_view(["GET"])
def get_advertiser_data(_):
    results = []
    advertisers = Advertiser.objects.all()

    try:
        for advertiser in advertisers:
            accepted_apis = advertiser.apis.filter(is_accepted=True)
            for api_entry in accepted_apis:
                cached = cache.get(f"advertiser_data_{api_entry.id}")
                if cached:
                    results.append(cached)
    except (ConnectionError, TimeoutError):
        # Redis not running
        return Response([])

    return Response(results)


@api_view(['POST'])
def advertiser_register(request):
    serializer = AdvertiserRegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Advertiser registered successfully."},
                        status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def advertiser_login(request):
    serializer = AdvertiserLoginSerializer(data=request.data)
    if serializer.is_valid():
        advertiser = serializer.validated_data['advertiser']
        token = get_tokens_for_user(advertiser)
        response = Response(status=status.HTTP_200_OK)
        response.set_cookie(key="auth_token", value=token, httponly=True)
        return response
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def submit_advertiser_api(request):
    token = request.COOKIES.get("auth_token")
    payload = is_user_authenticated(token)
    try:
        advertiser = Advertiser.objects.get(id=payload['id'])
    except Advertiser.DoesNotExist:
        return Response({"error": "Advertiser not found."}, status=status.HTTP_404_NOT_FOUND)
    serializer = AdvertiserAPISerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(advertiser=advertiser)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
