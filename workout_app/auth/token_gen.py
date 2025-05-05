import datetime
import os

import jwt


def get_tokens_for_user(user):
    payload = {
        'id': user.id,
        'exp': datetime.datetime.now() + datetime.timedelta(days=360)
    }
    token = jwt.encode(
        payload=payload, key=os.environ['JWTSECRET'], algorithm="HS256")
    return token
