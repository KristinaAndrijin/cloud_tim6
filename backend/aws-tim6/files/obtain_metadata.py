import json
import boto3
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('filesMetadata')

def convert_decimal_to_string(data):
    if isinstance(data, Decimal):
        return str(data)
    if isinstance(data, dict):
        return {key: convert_decimal_to_string(value) for key, value in data.items()}
    if isinstance(data, list):
        return [convert_decimal_to_string(item) for item in data]
    return data

def obtain_metadata(event, context):
    try:
        #user_info = event['requestContext']['authorizer']['claims']
        #username = user_info['preferred_username']
        request_body = json.loads(event['body'])
        obj_key_from_front = request_body['obj_key']

        #object_key = username + "/" + file_name
        object_key = obj_key_from_front

        response = table.get_item(
            Key={
                'object_key': object_key
            }
        )

        if 'Item' in response:
            metadata = response['Item']
            metadata = convert_decimal_to_string(metadata)
            return {
                "statusCode": 200,
                "body": json.dumps(metadata)
            }
        else:
            body = {
                "message": "Metadata not found for the given object key",
            }
            return {
                "statusCode": 404,
                "body": json.dumps(body)
            }

    except Exception as e:
        body = {
            "message": str(e),
        }
        return {"statusCode": 500, "body": json.dumps(body)}
