import boto3
import json

def delete_item(event, context):
    try:
        bucket_name = 'projekat6'
        metadata_table = 'filesMetadata'
        album_object_table = 'albumObject'
        user_files_table = 'userFiles'
        s3_client = boto3.client('s3')
        dynamodb = boto3.client('dynamodb')


        # Retrieve the file name from the request body
        request_body = json.loads(event['body'])
        object_key = request_body['object_key']
        user_info = event['requestContext']['authorizer']['claims']
        username = user_info['preferred_username']

        file_key_user = object_key.split("/")[0]
        print('radi')
        if file_key_user != username:
            body = {
                "message": "You cannot delete someone else's item!"
            }
            response = {
                'statusCode': 400,
                'body': json.dumps(body)
            }
            return response

        try:
            s3_client.delete_object(
                Bucket=bucket_name,
                Key=object_key
            )
            print('radi s3')
        except Exception as e:
            print('ne radi s3')
            print(e)
            return {
                "statusCode": 400,
                "body": f"Error occurred: {str(e)}"
            }
        try:
            dynamodb.delete_item(
                TableName=metadata_table,
                Key = {"object_key":{"S":object_key}}
            )
        except Exception as e:
            print('ne radi metadata')
            return {
                "statusCode": 400,
                "body": f"Error occurred: {str(e)}"
            }

        try:
            response = dynamodb.scan(
                TableName=album_object_table,
                Select='ALL_ATTRIBUTES',
                FilterExpression='object_key = :val',
                ExpressionAttributeValues={':val': {'S': object_key}}
            )
            for item in response["Items"]:
                key = {
                    'album_key': item['album_key'],
                    'object_key': item['object_key']
                }
                dynamodb.delete_item(
                    TableName=album_object_table,
                    Key=key
                )

        except Exception as e:
            print('ne radi albumObject')
            print(e)
            return {
                "statusCode": 400,
                "body": f"Error occurred: {str(e)}"
            }

        try:
            response = dynamodb.scan(
                TableName=user_files_table,
                Select='ALL_ATTRIBUTES',
                FilterExpression='file_key = :val',
                ExpressionAttributeValues={':val': {'S': object_key}}
            )
            for item in response["Items"]:
                key = {
                    'username': item['username'],
                    'file_key': item['file_key']
                }
                dynamodb.delete_item(
                    TableName=user_files_table,
                    Key=key
                )

        except Exception as e:
            print('ne radi userFiles')
            print(e)
            return {
                "statusCode": 400,
                "body": f"Error occurred: {str(e)}"
            }


        body = {
            "message": f"{object_key} deleted!"
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





