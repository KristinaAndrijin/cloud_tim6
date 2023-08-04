import json
import boto3

dynamodb = boto3.resource('dynamodb')

def write_metadata_upload(event, context):
    try:
        metadata_table = dynamodb.Table('filesMetadata')

        request_body = json.loads(event['body'])
        user_info = event['requestContext']['authorizer']['claims']
        username = user_info['preferred_username']

        item = {
            'object_key': username + "/" + request_body['name'],
            'name': request_body['name'],
            'type': request_body['type'],
            'size': request_body['size'],
            'upload_date': request_body['upload_date'],
            'tags': request_body['tags'],
            'description': request_body['description'],
        }

        response = metadata_table.put_item(
            Item=item,
            ConditionExpression='attribute_not_exists(object_key)'
        )

        body = {
            "message": "Metadata added successfully",
        }
        return {"statusCode": 200, "body": json.dumps(body)}



    except Exception as e:

        body = {
            "message": str(e),
        }
        return {"statusCode": 500, "body": json.dumps(body)}
