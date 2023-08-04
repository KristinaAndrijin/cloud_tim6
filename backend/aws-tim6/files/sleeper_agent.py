import json
import boto3
from constants import *

dynamodb = boto3.resource('dynamodb')
metadata_table = dynamodb.table('filesMetadata')
sqs = boto3.client('sqs')

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
