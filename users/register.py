import json
import logging
from bcrypt import hashpw, gensalt
from common.users.usermodel import User
from common.token.factory import create_user_token_as_string

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    try:
        logger.info(
            f'Register handler received event: {event} context: {context}')

        body = json.loads(event.get('body'))
        username = body.get('username')
        password = body.get('password')

        if not username or not password:
            raise ValueError(
                'Username and password is required for registration.')

        for user in User.username_index.query(username):
            raise ValueError(f'Username {user.User} already exists!')

        user = User(
            username=username,
            password_hash=
                hashpw(password.encode('utf-8'), gensalt()).decode('utf-8'))

        user.refresh_token = create_user_token_as_string(user, is_access_token=False)

        user.save()

        response = {
            "statusCode": 200,
            "body": json.dumps(
                {
                    'access_token': create_user_token_as_string(user),
                    'refresh_token': user.refresh_token
                }
            )
        }

        return response
    except Exception as e:
        logger.error(e, exc_info=True)
        raise Exception('Internal Server Error.')
