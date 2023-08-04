import json
import boto3
from constants import *


dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('userAlbum')
client = boto3.client('cognito-idp')


def give_access_to_album_to_user(event, context):
    # print('eee')
    if 'requestContext' in event and 'authorizer' in event['requestContext']:
        user_info = event['requestContext']['authorizer']['claims']
        owner = user_info['preferred_username']
        # print('owner')
        try:
            # dynamo db
            event_body = json.loads(event["body"])
            album_name = event_body.get("album_name")
            username = event_body.get("username")
            # print(album_name, username)
            all_users = get_users()
            # print(all_users)
            if username not in all_users:
                # print('tu je')
                body = {
                    "message": "User doesn't exist"
                }
                return {
                    'statusCode': 400,
                    'body': json.dumps(body)
                }
            album_key = owner + "/" + album_name
            item = {
                'username': username,
                'album_key': album_key
            }
            condition_expression = 'attribute_not_exists(username) AND attribute_not_exists(album_key)'
            table.put_item(Item=item, ConditionExpression=condition_expression)
            body = {
                "message": "Successfully inserted person!" ,
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
