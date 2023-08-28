import json


def hi():
    return "Go Serverless v3.0! Your function executed successfully!"

def hello(event, context):
    body = {
        "message": hi(),
        "input": event,
    }

    return {"statusCode": 200, "body": json.dumps(body)}
