import json
import logging
import sys
import traceback

import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('albumObject')

sqs = boto3.client('sqs')
album_object_queue_url = 'https://sqs.eu-central-1.amazonaws.com/275505252693/album-object-queue-real'

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def write_albumObject(event, context):

    object_key = event.get("object_key")
    response = sqs.receive_message(
        QueueUrl=album_object_queue_url,
        MaxNumberOfMessages=10
    )
    for message in response["Messages"]:
        item_str = message['Body']
        item = json.loads(item_str)
        item_ok = item["object_key"].replace(" ", "+")
        if object_key == item_ok:
            table.put_item(Item=item)
            sqs.delete_message(
                QueueUrl=album_object_queue_url,
                ReceiptHandle=message["ReceiptHandle"]
            )
            logger.info('deleted message?')
            break
