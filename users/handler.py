import logging
import json

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def get(event, context):
    logger.info(f'Received event: {event} context: {context}')

    try:
        return {
            'statusCode': 200,
            'body': 'Users test!',
            'headers': {}
        }
    except Exception as e:
        logger.error(e, exc_info=True)
        raise Exception('Unauthorized')
