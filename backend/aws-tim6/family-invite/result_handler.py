import json

def result_handler(event, context):
    code = event['statusCode']
    body = event['body']
    # TODO implement
    return {
        'statusCode': code,
        'body': body
    }
