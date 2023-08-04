import json
import boto3

sqs = boto3.client('sqs')

def write_metadata_upload(event, context):
    try:
        request_body = json.loads(event['body'])
        user_info = event['requestContext']['authorizer']['claims']
        username = user_info['preferred_username']

        item = {
            'object_key': username + "/" + request_body['name'],
            'name': request_body['name'],
            'type': request_body['type'],
            'size': request_body['size'],
            'upload_date': request_body['upload_date'],
            'tags': request_body['tags'],
            'description': request_body['description'],
        }

        # Send the item as a message to the SQS queue
        sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=json.dumps(item)
        )

        body = {
            "message": "Metadata added to SQS queue successfully",
        }
        return {"statusCode": 200, "body": json.dumps(body)}

    except Exception as e:
        body = {
            "message": str(e),
        }
        return {"statusCode": 500, "body": json.dumps(body)}

