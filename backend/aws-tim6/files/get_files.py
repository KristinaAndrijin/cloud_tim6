import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('albumObject')


def get_files_by_album(event, context):
    if 'requestContext' in event and 'authorizer' in event['requestContext']:
        user_info = event['requestContext']['authorizer']['claims']
        username = user_info['preferred_username']
        try:
            response = table.scan()

            items = response['Items']
            while 'LastEvaluatedKey' in response:
                response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
                items.extend(response['Items'])
            albums = []
            for item in items:
                if item['album_key'] == username:
                    albums.append(item['album_key'])
            print(albums)
            body = {
                "message": "Successful",
                "albums": albums
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

        response = table.scan()

        items = response['Items']
        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
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