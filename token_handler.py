import json
import logging
from token_validator.validator import validate, generate_aws_policy


logger = logging.getLogger()
logger.setLevel(logging.INFO)


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
