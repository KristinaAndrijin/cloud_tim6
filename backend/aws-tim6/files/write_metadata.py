import json
import logging
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('filesMetadata')

sqs = boto3.client('sqs')
metadata_queue_url = 'https://sqs.eu-central-1.amazonaws.com/275505252693/metadata-queue'

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def write_metadata(event, context):

    object_key = event.get("object_key").replace(" ", "+")
    response = sqs.receive_message(
        QueueUrl=metadata_queue_url,
        MaxNumberOfMessages=10
    )
    for message in response["Messages"]:
        item_str = message['Body']
        item = json.loads(item_str)
        item_ok = item["object_key"].replace(" ", "+")
        if object_key == item_ok:

            if item["replaces"] and item["replaces"].replace(" ", "+") != item_ok:
                replace_helper(item)

            else:
                table.put_item(Item=item)
                sqs.delete_message(
                    QueueUrl=metadata_queue_url,
                    ReceiptHandle=message["ReceiptHandle"]
                )
                logger.info('deleted message?')
                break

def replace_helper (item):
    pass
