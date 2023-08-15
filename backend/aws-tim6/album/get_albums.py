import json
import boto3

dynamodb = boto3.resource('dynamodb')
user_album_table = dynamodb.Table('userAlbum')


def get_albums_by_user(event, context):
    if 'requestContext' in event and 'authorizer' in event['requestContext']:
        user_info = event['requestContext']['authorizer']['claims']
        username = user_info['preferred_username']
        try:

            event_body = json.loads(event["body"])
            album_name = event_body.get("album_name")

            response = user_album_table.scan()
            items = response['Items']
            while 'LastEvaluatedKey' in response:
                response = user_album_table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
                items.extend(response['Items'])

            albums_small = []
            albums = []
            for item in items:
                album_key = item['album_key']
                if (item['username'] == username or album_key.split('/')[0] == username):
                    # if '/' in album_key:
                    #     albums = ...
                    albums_small.append(album_key)
            print('albums_small', albums_small)

            #'', owner + '/'
            found = False
            if album_name == '' or album_name == username + '/':
                found = True
            if not found:
                for album in albums_small:
                    if album_name.startswith(album) or album_name == '' or album :
                        found = True
            if not found:
                body = {
                        "message": "Can't view album " + album_name,
                }
                return {"statusCode": 403, "body": json.dumps(body)}

            for item in items:
                album_key = item['album_key']
                for album in albums_small:
                    if album in album_key and album_key.startswith(album_name) and album_key not in albums:
                        albums.append(album_key)
            print('albums', albums)
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


def get_users_by_album(event, context):
    try:

        event_body = json.loads(event["body"])
        album_name = event_body.get("album_name")

        response = user_album_table.scan()

        items = response['Items']
        while 'LastEvaluatedKey' in response:
            response = user_album_table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
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