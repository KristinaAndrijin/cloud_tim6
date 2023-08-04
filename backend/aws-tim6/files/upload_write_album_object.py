import json
import boto3

dynamodb = boto3.resource('dynamodb')


def write_album_object(event, context):
    try:
        album_object_table = dynamodb.Table('albumObject')

        request_body = json.loads(event['body'])
        user_info = event['requestContext']['authorizer']['claims']
        username = user_info['preferred_username']

        item = {
            'object_key': username + "/" + request_body['file_name'],
            'album_key': request_body['album_key'],
        }

        response = album_object_table.put_item(
            Item=item,
        )

        body = {
            "message": "Album data added successfully",
        }
        return {"statusCode": 200, "body": json.dumps(body)}

    except Exception as e:
        body = {
            "message": str(e),
        }
        return {"statusCode": 500, "body": json.dumps(body)}
