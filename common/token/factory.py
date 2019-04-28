from datetime import datetime, timedelta
import jwt
import os
from ..users.usermodel import User


def create_user_token(user):
    payload = {
        'exp': datetime.utcnow() + timedelta(days=1),
        'iat': datetime.utcnow(),
        'sub': user.user_id
    }

    return jwt.encode(
        payload,
        os.environ.get('SECRET_KEY'),
        algorithm='HS256'
    )


def validate_user_token(token):
    return jwt.decode(
        jwt=token,
        key=os.environ.get('SECRET_KEY'),
        algorithms=['HS256'])
