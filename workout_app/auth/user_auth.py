import os
import jwt


def is_user_authenticated(token):
    if not token:
        return None
    try:
        payload = jwt.decode(
            token, key=os.environ['JWTSECRET'], algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
