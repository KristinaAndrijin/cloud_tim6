import json
import boto3

dynamodb = boto3.resource('dynamodb')
album_object_table = dynamodb.Table('albumObject')


def get_files_by_album(event, context):
    if 'requestContext' in event and 'authorizer' in event['requestContext']:
        user_info = event['requestContext']['authorizer']['claims']
        username = user_info['preferred_username']
        try:
            response = album_object_table.scan()

            event_body = json.loads(event["body"])
            album_name = event_body.get("album_name")

            requested_username = album_name.split('/')[0]
            if requested_username != username:
                body = {
                    "message": "Can't view this!",
                }
                return {"statusCode": 403, "body": json.dumps(body)}

            items = response['Items']
            while 'LastEvaluatedKey' in response:
                response = album_object_table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
                items.extend(response['Items'])
            files = []
            for item in items:
                if item['album_key'] == album_name:
                    # print(item['album_key'])
                    object_key = item['object_key']
                    owner, name = object_key.split('/')
                    files.append({'owner': owner, 'name': name, 'upload_date': item['upload_date']})
            print('files ', files)
            body = {
                "message": "Successful",
                "files": files
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