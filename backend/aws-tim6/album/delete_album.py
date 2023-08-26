import json
import boto3
import logging
import sys
import traceback

dynamodb = boto3.client('dynamodb')
user_album_table = 'userAlbum'
object_album_table = 'albumObject'

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def delete_album(event, context):
    if 'requestContext' in event and 'authorizer' in event['requestContext']:
        user_info = event['requestContext']['authorizer']['claims']
        username = user_info['preferred_username']
        try:
            event_body = json.loads(event["body"])
            album_name = event_body.get("album_name")
            if album_name == username:
                body = {
                    "message": "Cannot delete default album!",
                }
                return {"statusCode": 400, "body": json.dumps(body)}

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

        except Exception as exp:
            exception_type, exception_value, exception_traceback = sys.exc_info()
            traceback_string = traceback.format_exception(exception_type, exception_value, exception_traceback)
            err_msg = json.dumps({
                "errorType": exception_type.__name__,
                "errorMessage": str(exception_value),
                "stackTrace": traceback_string})
            logger.error(err_msg)
    else:
        body = {
            "message": "Missing token",
        }
        return {"statusCode": 401, "body": json.dumps(body)}


def delete_album_content_and_permissions(album_name):
    objects = get_all_album_objects(album_name)
    if len(objects) > 0:
        for object_key in objects:
            print(object_key)
            count = count_references(object_key)
            if count <= 1:
                fully_delete_object(object_key)
            dynamodb.delete_item(
                TableName=object_album_table,
                Key={
                    "album_key": {"S": album_name},
                    "object_key": object_key
                }
            )
    users = get_usernames_by_album_key(album_name)
    if len(users) > 0:
        for username in users:
            dynamodb.delete_item(
                TableName=user_album_table,
                Key={
                    "username": username,
                    "album_key": {"S": album_name}
                }
            )

def get_all_album_objects(album_key):
    all_object_keys_in_album = []
    response = dynamodb.query(
        TableName=object_album_table,
        KeyConditionExpression='album_key = :album_key',
        ExpressionAttributeValues={':album_key': {"S": album_key}},
        ProjectionExpression='object_key'
    )
    for item in response['Items']:
        all_object_keys_in_album.append(item['object_key'])

    return all_object_keys_in_album


def count_references(object_key):
    response = dynamodb.scan(
        TableName=object_album_table,
        FilterExpression='object_key = :object_key',
        ExpressionAttributeValues={':object_key': object_key}
    )
    count = response['Count']
    return count


def fully_delete_object(object_key):
    s3 = boto3.client("s3")

    s3.delete_object(Bucket='projekat6', Key=object_key["S"])
    dynamodb.delete_item(
        TableName="filesMetadata",
        Key={
            "object_key": object_key
        }
    )


def get_usernames_by_album_key(album_key):
    response = dynamodb.scan(
        TableName=user_album_table,
        FilterExpression='album_key = :album_key',
        ExpressionAttributeValues={':album_key': {"S": album_key}},
        ProjectionExpression='username'
    )

    usernames = [item['username'] for item in response['Items']]
    return usernames


def find_album_keys_with_prefix(album_prefix):
    response = dynamodb.scan(
        TableName=user_album_table,
        FilterExpression='begins_with(album_key, :prefix)',
        ExpressionAttributeValues={':prefix': {"S": album_prefix}},
        ProjectionExpression='album_key'
    )

    album_keys = [item['album_key'] for item in response['Items']]
    return album_keys



