import json
import boto3

dynamodb = boto3.resource('dynamodb')
sqs = boto3.client('sqs')

def write_album_object(event, context):
    try:
        album_object_table = dynamodb.Table('albumObject')
        queue_url = 'https://sqs.eu-central-1.amazonaws.com/275505252693/album-object-queue-real'

        request_body = json.loads(event['body'])
        user_info = event['requestContext']['authorizer']['claims']
        username = user_info['preferred_username']

        item = {
            'object_key': username + "/" + request_body['file_name'],
            'album_key': request_body['album_key'],
            'upload_date': request_body['upload_date'],
        }

        # Send the item as a message to the SQS queue
        sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=json.dumps(item)
        )

        # response = album_object_table.put_item(
        #     Item=item,
        # )

        body = {
            "message": "Album data added successfully to queue",
        }
        return {"statusCode": 200, "body": json.dumps(body)}

    except Exception as e:
        body = {
            "message": str(e),
        }
        return {"statusCode": 500, "body": json.dumps(body)}
