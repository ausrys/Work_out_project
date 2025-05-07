import os
import jwt
from rest_framework.response import Response
from rest_framework import status


def is_user_authenticated(token):
    if not token:
        return Response({'error': 'Unauthenticated, please log in'},
                        status=status.HTTP_400_BAD_REQUEST)
    try:
        payload = jwt.decode(
            token, key=os.environ['JWTSECRET'], algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return Response({'error': 'Unauthenticated, please log in'},
                        status=status.HTTP_400_BAD_REQUEST)
    return payload
