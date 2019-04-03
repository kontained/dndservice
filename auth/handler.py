import jwt
import os
import json
import logging


def authorize(event, context):
    logging.info(f'Received event: {event} context: {context}')

    token = event.get('authorizationToken')[7:]

    if token is None:
        logging.error('Token not found, exiting')
        raise Exception('Unauthorized')

    try:
        payload = validate(token)
        return generate_aws_policy(payload.get('sub'), 'Allow', event.get('methodArn'))
    except Exception as e:
        logging.error(e, exc_info=True)
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
                }]
        }
    }