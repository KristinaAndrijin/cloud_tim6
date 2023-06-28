import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('userAlbum')
client = boto3.client('cognito-idp')
user_pool_id = 'eu-central-1_JTv6FBTKX'

def remove_access_to_album_from_user(event, context):
    if 'requestContext' in event and 'authorizer' in event['requestContext']:
        user_info = event['requestContext']['authorizer']['claims']
        owner = user_info['preferred_username']
        try:
            # dynamo db
            event_body = json.loads(event["body"])
            album_name = event_body.get("album_name")
            username = event_body.get("username")
            if username not in get_users():
                body = {
                    "message": "User doesn't exist"
                }
                return {
                    'statusCode': 400,
                    'body': json.dumps(body)
                }
            
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
    
    
    
def get_users():
    # print('hej')
    users_ret = []
    response = client.list_users(
        UserPoolId=user_pool_id
    )
    users = response['Users']
    for user in users:
        attributes = user['Attributes']
        for att in attributes:
            name = att['Name']
            # print('name', name)
            value = att['Value']
            # print('value', value)
            if (name == 'preferred_username'):
                users_ret.append(value)
                # print(users_ret)
    # print(users_ret)
    return users_ret