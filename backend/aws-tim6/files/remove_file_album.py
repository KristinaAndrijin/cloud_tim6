import boto3
import json

album_object_table = "albumObject"

def remove_file_album(event, lambda_context):
    try:
        request_body = json.loads(event['body'])
        file_name = request_body['file_name']
        user_info = event['requestContext']['authorizer']['claims']
        username = user_info['preferred_username']
        album_name = request_body['album_name']
        dynamodb = boto3.client('dynamodb')

        file_key_user = album_name.split("/")[0]
        print('radi')

        if file_key_user != username:
            body = {
                "message": "You cannot delete from someone else's album!"
            }
            response = {
                'statusCode': 400,
                'body': json.dumps(body)
            }
            return response

        key = {
            'album_key': {'S': album_name},
            'object_key': {'S': file_name}
        }
        dynamodb.delete_item(
            TableName=album_object_table,
            Key=key
        )

        response = dynamodb.scan(
            TableName=album_object_table,
            Select='ALL_ATTRIBUTES',
            FilterExpression='object_key = :val',
            ExpressionAttributeValues={':val': {'S': file_name}}
        )

        if len(response["Items"]) == 0:

            item = {
                'album_key': {'S': username},
                'object_key': {'S': file_name},
                'upload_date': {'S': request_body['upload_date']},
            }

            dynamodb.put_item(TableName=album_object_table, Item=item)

        body = {
            "message": f"{file_name} removed from {album_name}!"
        }
        response = {
            'statusCode': 200,
            'body': json.dumps(body)
        }

        return response


    except Exception as e:
        return {
            "statusCode": 400,
            "body": f"Error occurred: {str(e)}"
        }