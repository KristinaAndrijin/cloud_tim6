import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('userAlbum')

def remove_access_to_album_from_user(event, context):
    if 'requestContext' in event and 'authorizer' in event['requestContext']:
        user_info = event['requestContext']['authorizer']['claims']
        owner = user_info['preferred_username']
        try:
            # dynamo db
            event_body = json.loads(event["body"])
            album_name = event_body.get("album_name")
            username = event.body.get("username")
            album_key = owner + "/" + album_name
            
            
            response = table.get_item(
                Key={
                    'username': username,
                    'album_key': album_key
                }
            )

            if 'Item' in response:
                
                # dynamo
                response = table.delete_item(
                    Key={
                        'username': username,
                        'album_key': album_key
                    }
                )

                if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                    body = {
                        "message": "Successful removal of access to album " + album_key,
                        "response": str(response)
                    }
                    return {"statusCode": 200, "body": json.dumps(body)}
                else:
                    body = {
                        "message": "Item wasnt deleted!",
                        "response": str(response)
                    }
                    return {"statusCode": 400, "body": json.dumps(body)}
            else:
                body = {
                    "message": "Item NOT found, user " + username + " does not access to album " + album_key,
                }
                return {"statusCode": 404, "body": json.dumps(body)}

        
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