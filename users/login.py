import json
import logging
from bcrypt import hashpw, checkpw
from common.users.usermodel import User
from common.token.factory import create_user_token_as_string

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    try:
        logger.info(f'Received event: {event} context: {context}')

        body = json.loads(event.get('body'))
        username = body.get('username')
        password = body.get('password')

        if not username or not password:
            raise ValueError('username and password is required for login.')

        for result in User.username_index.query(username, limit=1):
            user = result
            break

        if not checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
            raise ValueError('password is invalid.')

        response = {
            "statusCode": 200,
            "body": json.dumps(
                {
                    'access_token': create_user_token_as_string(user)
                }
            )
        }

        return response
    except Exception as e:
        logger.error(e, exc_info=True)
        raise Exception('Internal Server Error.')
