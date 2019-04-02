import jwt
import os


def validate(token):
    return jwt.decode(
        jwt=token,
        key='123456789',
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
