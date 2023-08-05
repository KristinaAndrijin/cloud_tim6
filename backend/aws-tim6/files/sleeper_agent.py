import json
import logging
import sys
import traceback

import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('filesMetadata')
sqs = boto3.client('sqs')
queue_url = 'https://sqs.eu-central-1.amazonaws.com/275505252693/metadata-queue'


logger = logging.getLogger()
logger.setLevel(logging.INFO)

def sleeper_agent(event, context):
    try:
        object_key = event["Records"][0]["s3"]["object"]["key"]
        logger.info(f'object_key: {object_key}')
        response = sqs.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=10
        )
        for message in response["Messages"]:
            item_str = message['Body']
            logger.info(f'item_json: {item_str}')
            item = json.loads(item_str)
            if(object_key == item["object_key"]):
                table.put_item(Item=item)
                sqs.delete_message(
                    QueueUrl=queue_url,
                    ReceiptHandle=message["ReceiptHandle"]
                )
                logger.info('deleted message?')


    except Exception as exp:
        exception_type, exception_value, exception_traceback = sys.exc_info()
        traceback_string = traceback.format_exception(exception_type, exception_value, exception_traceback)
        err_msg = json.dumps({
        "errorType": exception_type.__name__,
        "errorMessage": str(exception_value),
        "stackTrace": traceback_string})

        logger.error(err_msg)
