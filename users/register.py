import json
import logging
from bcrypt import hashpw, gensalt
from users.models.user import User

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    try:
        logger.info(f'Received event: {event} context: {context}')

        body = event.get('body')

        username = body.get('username')
        password_hash = hashpw(body.get('password'), gensalt())

        body = {
            'username': username,
            'password_hash': password_hash
        }

        #if username:
        #   for user in User.username_index.query(body.get('username')):
        #        raise Exception(f'Username {user.User} already exists!')

        response = {
            "statusCode": 200,
            "body": json.dumps(body)
        }

        return response
    except Exception as e:
        logger.error(e, exc_info=True)
        raise Exception('Internal Server Error.')
