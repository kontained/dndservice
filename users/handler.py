import logging
import json


def get(event, context):
    logging.info(f'Received event: {event} context: {context}')

    try:
        return json.dumps(event)
    except Exception as e:
        logging.error(e, exc_info=True)
        raise Exception('Unauthorized')
