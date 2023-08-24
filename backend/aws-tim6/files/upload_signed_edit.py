import json
import boto3

def generate_signed_url_edit(event, context):
    try:
        bucket_name = 'projekat6'
        s3_client = boto3.client('s3')

        request_body = json.loads(event['body'])
        obj_key = request_body['obj_key']
        content_type = request_body['contentType']
        user_info = event['requestContext']['authorizer']['claims']
        username = user_info['preferred_username']

        file_key_user = object_key.split("/")[0]
        if file_key_user != username:
            body = {
                "message": "You cannot edit someone else's item!"
            }
            response = {
                'statusCode': 400,
                'body': json.dumps(body)
            }
            return response

        # Generate a presigned URL for uploading the file
        signed_url = s3_client.generate_presigned_url(
            'put_object',
            Params={'Bucket': bucket_name, 'Key': obj_key, 'ContentType': content_type},
            ExpiresIn=3600  # URL expiration time in seconds (adjust as needed)
        )

        # Return the signed URL as the response
        response = {
            'statusCode': 200,
            'body': json.dumps({
                'signedUrl': signed_url,
                'key': key
            }),
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Credentials': True
            }
        }
        
        return response

    except Exception as e:
        return {
            "statusCode": 400,
            "body": f"Error occurred: {str(e)}"
        }
