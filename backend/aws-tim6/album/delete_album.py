import json
import boto3

dynamodb = boto3.resource('dynamodb')
user_album_table = dynamodb.Table('userAlbum')
object_album_table = dynamodb.Table('albumObject')

def delete_album(event, context):
    if 'requestContext' in event and 'authorizer' in event['requestContext']:
        user_info = event['requestContext']['authorizer']['claims']
        username = user_info['preferred_username']
        try:
            event_body = json.loads(event["body"])
            album_name = event_body.get("album_name")
            if album_name.startswith(username):
                delete_album_content_and_permissions(album_name)
                sub_albums = find_album_keys_with_prefix(album_name)
                for album in sub_albums:
                    delete_album_content_and_permissions(album)
                body = {
                    "message": "Deleted album!",
                }
                return {"statusCode": 200, "body": json.dumps(body)}
            else:
                body = {
                    "message": "Can't delete someone else's album!",
                }
                return {"statusCode": 403, "body": json.dumps(body)}

        except:
            pass
    else:
        body = {
            "message": "Missing token",
        }
        return {"statusCode": 401, "body": json.dumps(body)}


def delete_album_content_and_permissions(album_name):
    objects = get_all_album_objects(album_name)
    if objects.len() > 0:
        for object_key in objects:
            count = count_references(object_key)
            if count == 1:
                fully_delete_object(object_key)
            object_album_table.delete_item(
                Key={
                    "album_key": {'S': album_name},
                    "object_key": {'S': object_key}
                }
            )
    users = get_usernames_by_album_key(album_name)
    if users.len() > 0:
        for username in users:
            user_album_table.delete_item(
                Key={
                    "username": {"S": username},
                    "album_key": {"S": album_name}
                }
            )


def get_all_album_objects(album_key):
    all_object_keys_in_album = []
    response = object_album_table.query(
        KeyConditionExpression='album_key = :album_key',
        ExpressionAttributeValues={':album_key': album_key},
        ProjectionExpression='object_key'
    )
    for item in response['Items']:
        all_object_keys_in_album.append(item['object_key'])

    return all_object_keys_in_album

def count_references(object_key):
    response = object_album_table.scan(
        FilterExpression='object_key = :object_key',
        ExpressionAttributeValues={':object_key': object_key}
    )
    count = response['Count']
    return count

def fully_delete_object(object_key):
    s3 = boto3.resource("s3")
    fileMetadata = boto3.resource("dynamodb").Table("fileMetadata")

    s3.delete_object(Bucket='projekat6', Key=object_key)
    fileMetadata.delete_item(
        Key={
            "object_key": {'S': object_key}
        }
    )

def get_usernames_by_album_key(album_key):

    response = user_album_table.query(
        IndexName='album_key-index',
        KeyConditionExpression='album_key = :album_key',
        ExpressionAttributeValues={':album_key': album_key},
        ProjectionExpression='username'
    )

    usernames = [item['username'] for item in response['Items']]
    return usernames

def find_album_keys_with_prefix(album_prefix):

    response = user_album_table.scan(
        FilterExpression='begins_with(album_key, :prefix)',
        ExpressionAttributeValues={':prefix': album_prefix},
        ProjectionExpression='album_key'
    )

    album_keys = [item['album_key'] for item in response['Items']]
    return album_keys



