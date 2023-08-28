import json
import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
album_object_table = dynamodb.Table('albumObject')
user_file_table = dynamodb.Table('userFiles')
user_album_table = dynamodb.Table('userAlbum')


def get_files_by_album(event, context):

    if 'requestContext' in event and 'authorizer' in event['requestContext']:
        user_info = event['requestContext']['authorizer']['claims']
        username = user_info['preferred_username']
        try:
            event_body = json.loads(event["body"])
            album_name = event_body.get("album_name")

            files = []
            album_keys = []

            response = user_file_table.scan()
            items = response['Items']
            while 'LastEvaluatedKey' in response:
                response = album_object_table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
                items.extend(response['Items'])
            files_keys = []
            for item in items:
                if item['username'] == username or item['file_key'].split('/')[0] == username:
                    files_keys.append(item['file_key'])
            print('files_keys', files_keys)
            if album_name == username:
                # files = files_keys
                pass
            else:
                response = user_album_table.scan()
                items = response['Items']
                while 'LastEvaluatedKey' in response:
                    response = album_object_table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
                    items.extend(response['Items'])
                albums_small = []
                for item in items:
                    if item['username'] == username or item['album_key'].split('/')[0] == username:
                        albums_small.append(item['album_key'])
                for item in items:
                    album_key = item['album_key']
                    for album in albums_small:
                        if album in album_key and album_key not in album_keys:
                            album_keys.append(album_key)
                # requested_username = album_name.split('/')[0]
                # if requested_username != username:
                #     body = {
                #         "message": "Can't view this!",
                #     }
                #     return {"statusCode": 403, "body": json.dumps(body)}
            response = album_object_table.scan()
            items = response['Items']
            while 'LastEvaluatedKey' in response:
                response = album_object_table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
                items.extend(response['Items'])
            for item in items:
                if (item['album_key'] == album_name and album_name in album_keys) or (album_name == username and item['object_key'] in files_keys) or (item['album_key']==username and album_name == username):
                    # print(item['album_key'])
                    object_key = item['object_key']
                    owner, name = object_key.split('/')
                    if {'owner': owner, 'name': name, 'upload_date': item['upload_date']} in files:
                        continue;
                    files.append({'owner': owner, 'name': name, 'upload_date': item['upload_date']})

            # files.append({'owner': 'rkis', 'name': 'n', 'upload_date': '18.10.2000. 19:46:18'})
            print('files ', files)
            sorted_files = sorted(files, key=lambda x: datetime.strptime(x['upload_date'], '%d.%m.%Y. %H:%M:%S'))
            print('sorted', sorted_files)
            body = {
                "message": "Successful",
                "files": sorted_files
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


def get_users_by_files(event, context):
    try:

        event_body = json.loads(event["body"])
        album_name = event_body.get("album_name")

        response = album_object_table.scan()

        items = response['Items']
        while 'LastEvaluatedKey' in response:
            response = album_object_table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            items.extend(response['Items'])
        users = []
        for item in items:
            if item['album_key'] == album_name:
                users.append(item['username'])
        print(users)
        body = {
            "message": "Successful",
            "users_with_access": users
        }
        return {"statusCode": 200, "body": json.dumps(body)}
    except Exception as e:
        return {
            "statusCode": 400,
            "body": f"Error occurred: {str(e)}"
        }