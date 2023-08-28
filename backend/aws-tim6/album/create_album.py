import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('userAlbum')


def create_album(event, context):
    if 'requestContext' in event and 'authorizer' in event['requestContext']:
        user_info = event['requestContext']['authorizer']['claims']
        username = user_info['preferred_username']
        try:
            # dynamo db
            event_body = json.loads(event["body"])
            album_name = event_body.get("album_name")
            album_key = username + "/" + album_name
            item = {
                'username': username,
                'album_key': album_key
            }
            condition_expression = 'attribute_not_exists(username) AND attribute_not_exists(album_key)'
            table.put_item(Item=item, ConditionExpression=condition_expression)
            body = {
                "message": "Successfully inserted person!",
                "username": username,
                "album_key": album_key
            }
            return {"statusCode": 200, "body": json.dumps(body)}

        except dynamodb.meta.client.exceptions.ConditionalCheckFailedException:
            body = {
                "message": "Item already exists"
            }
            return {
                'statusCode': 400,
                'body': json.dumps(body)
            }
        except Exception as e:
            return {
                "statusCode": 400,
                "body": f"Error occurred: {str(e)}"
            }

    else:
        body = {
            "message": "Missing token",
        }
        return {"statusCode": 401, "body": json.dumps(body)}