import jwt
import os
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    try:
        logger.info(f'Received event: {event} context: {context}')

        token = event.get('authorizationToken')[7:]

        if token is None:
            logger.error('Token not found, exiting')
            raise Exception('Token not found')

        payload = validate(token)
        policy = generate_aws_policy(payload.get('sub'), 'Allow', event.get('methodArn'))
        logger.info(f'Returning policy: {policy}')
        return policy
    except Exception as e:
        logger.error(e, exc_info=True)
        raise Exception('Unauthorized')


def validate(token):
    return jwt.decode(
        jwt=token,
        key=os.environ.get('SECRET_KEY'),
        algorithms=['HS256'])


def generate_aws_policy(principal_id, effect, resource):
    return {
        'principalId': principal_id,
        'policyDocument': {
            'Version': '2012-10-17',
            'Statement': [
                {
                    "Action": "execute-api:Invoke",
                    "Effect": effect,
                    "Resource": resource

                }
            ]
        }
    }
