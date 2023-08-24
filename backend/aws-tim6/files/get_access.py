import json
import boto3

dynamodb = boto3.resource('dynamodb')
user_album_table = dynamodb.Table('userAlbum')
user_file_table = dynamodb.Table('userFiles')
album_object_table = dynamodb.Table('albumObject')
client = boto3.client('cognito-idp')
user_pool_id = 'eu-central-1_N333IcKgF'


def get_access_by_user_file(event, context):
    if 'requestContext' in event and 'authorizer' in event['requestContext']:
        user_info = event['requestContext']['authorizer']['claims']
        username = user_info['preferred_username']
        try:

            event_body = json.loads(event["body"])
            album_name = event_body.get("album_name")
            file_key = event_body.get('file_key')

            users_with_access = []
            postponed_access = []

            response = album_object_table.get_item(
                Key={
                    'album_key': album_name,
                    'object_key': file_key
                }
            )

            if 'Item' not in response:
                body = {
                    "message": "Item NOT found, this file is not in this album or one of them doesn't exist etc!",
                }
                return {"statusCode": 404, "body": json.dumps(body)}


            response = user_album_table.scan()
            items = response['Items']
            while 'LastEvaluatedKey' in response:
                response = user_album_table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
                items.extend(response['Items'])

            for item in items:
                item_username = item['username']
                item_album_key = item['album_key']
                if item_album_key == album_name and item_username != username:
                    postponed_access.append(item_username)

            response = user_file_table.scan()
            items = response['Items']
            while 'LastEvaluatedKey' in response:
                response = user_album_table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
                items.extend(response['Items'])

            for item in items:
                item_username = item['username']
                item_file_key = item['file_key']
                if item_file_key == file_key and item_username != username:
                    users_with_access.append(item_username)


            print('users')
            print(users_with_access)

            all_users = get_users()
            print('all')
            print(all_users)
            permissions = []
            for user in all_users:
                if user == username:
                    continue
                if user in users_with_access and user not in postponed_access:
                    permissions.append({'username': user, 'access': True, 'hasAccess': True})
                elif user not in users_with_access and user not in postponed_access:
                    permissions.append({'username': user, 'access': True, 'hasAccess': False})
                else:
                    permissions.append({'username': user, 'access': False, 'hasAccess': False})
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