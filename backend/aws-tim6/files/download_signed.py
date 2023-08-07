import json
import boto3

def generate_signed_url(event, context):
    try:
        bucket_name = 'projekat6'
        s3_client = boto3.client('s3')

        # Retrieve the file name from the request body
        request_body = json.loads(event['body'])
        file_name = request_body['fileName']

        # Specify the S3 bucket and key for the file
        key = file_name  # Adjust the key as needed

        # Generate a presigned URL for downloading the file
        signed_url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket_name, 'Key': key},
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
