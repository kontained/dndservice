import json


def get(event, context):
    body = {
        "message": "Test get!",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response
