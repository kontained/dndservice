import jwt
import os
import json
import logging
from common.token.factory import validate_user_token

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    try:
        logger.info(f'Received event: {event} context: {context}')
        token = event.get('authorizationToken')[7:]
        payload = validate_user_token(token)
        policy = generate_aws_policy(payload.get('sub'), 'Allow', event.get('methodArn'))
        logger.info(f'Returning policy: {policy}')
        return policy
    except Exception as e:
        logger.error(e, exc_info=True)
        raise Exception('Unauthorized')


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
