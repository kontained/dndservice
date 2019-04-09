import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    try:
        logger.info(f'Received event: {event} context: {context}')

        body = {
            "message": "Hello from users/login!!",
            "input": event
        }

        response = {
            "statusCode": 200,
            "body": json.dumps(body)
        }

        return response
    except Exception as e:
        logger.error(e, exc_info=True)
