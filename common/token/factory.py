from datetime import datetime, timedelta
import jwt
import os
from ..users.usermodel import User


def create_user_token(user, is_access_token=True):
    payload = {
        'exp': datetime.utcnow() + timedelta(days=1),
        'iat': datetime.utcnow(),
        'sub': user.user_id
    }

    return jwt.encode(
        payload,
        os.environ.get('SECRET_KEY') if is_access_token else os.environ.get('REFRESH_KEY'),
        algorithm='HS256'
    )


def create_user_token_as_string(user, is_access_token=True):
    token = create_user_token(user, is_access_token)
    return token.decode('utf-8')


def validate_user_token(token, is_access_token=True):
    return jwt.decode(
        jwt=token,
        key=os.environ.get('SECRET_KEY') if is_access_token else os.environ.get('REFRESH_KEY'),
        algorithms=['HS256'])
