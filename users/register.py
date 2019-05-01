import json
import logging
from bcrypt import hashpw, gensalt
from common.users.usermodel import User
from common.token.factory import create_user_token

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

        if username:
            for user in User.username_index.query(body.get('username')):
                raise ValueError(f'Username {user.User} already exists!')

        user = User(
            username=username,
            password_hash=hashpw(body.get('password').encode(), gensalt()))

        token = create_user_token(user)

        response = {
            "statusCode": 200,
            "body": json.dumps(
                {
                    'user_id': user.user_id,
                    'token': token.decode('utf-8')
                }
            )
        }

        return response
    except Exception as e:
        logger.error(e, exc_info=True)
        raise Exception('Internal Server Error.')
