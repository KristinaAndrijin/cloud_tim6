import json
import boto3

dynamodb = boto3.resource('dynamodb')
metadata_table = dynamodb.table('filesMetadata')
sqs = boto3.client('sqs')
queue_url = 'https://sqs.eu-central-1.amazonaws.com/275505252693/metadata-queue'

def sleeper_agent(event, context):
    try:
        response = sqs.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=1
        )

        item_json = json.loads(response[0])

        metadata_table.put_item(Item=item_json)

    except Exception as e:

        body = {
            "message": str(e),
        }
        return {"statusCode": 500, "body": json.dumps(body)}
