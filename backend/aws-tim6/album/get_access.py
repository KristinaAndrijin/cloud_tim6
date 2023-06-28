import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('userAlbum')
client = boto3.client('cognito-idp')
user_pool_id = 'eu-central-1_JTv6FBTKX'


def get_access_by_user_album(event, context):
    if 'requestContext' in event and 'authorizer' in event['requestContext']:
        user_info = event['requestContext']['authorizer']['claims']
        username = user_info['preferred_username']
        try:
        
            event_body = json.loads(event["body"])
            album_name = event_body.get("album_name")
            
            response = table.scan()
        
            items = response['Items']
            while 'LastEvaluatedKey' in response:
                response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
                items.extend(response['Items'])
            users_with_access = []
            for item in items:
                if item['album_key'] == album_name and item['username'] != username:
                    users_with_access.append(item['username'])
            print('users')
            print(users_with_access)
            
            all_users = get_users()
            print('all')
            print(all_users)
            permissions = []
            for user in all_users:
                if user == username:
                    continue
                if user in users_with_access:
                    permissions.append({'username': user, 'hasAccess': True})
                else:
                    permissions.append({'username': user, 'hasAccess': False})
            print('permissions')
            print(permissions)
            if len(permissions) != 0:
                body = {
                    "message": "Successful",
                    "permissions": permissions
                }
                return {"statusCode": 200, "body": json.dumps(body)}
            else:
                body = {
                    "message": "Not found"
                }
                return {"statusCode": 404, "body": json.dumps(body)}  
            body = {
                "message": "Successful"
            }
            return {"statusCode": 200, "body": json.dumps(body)}
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