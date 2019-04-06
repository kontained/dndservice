import json


def get(event, context):
    body = {
        "message": "Hello from get users!!",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response
