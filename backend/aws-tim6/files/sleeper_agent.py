import json
import logging
import sys
import traceback

import boto3

dynamodb = boto3.resource('dynamodb')
metadata_table = dynamodb.Table('filesMetadata')
album_object_table = dynamodb.Table('albumObject')

sqs = boto3.client('sqs')
metadata_queue_url = 'https://sqs.eu-central-1.amazonaws.com/275505252693/metadata-queue'
album_object_queue_url = 'https://sqs.eu-central-1.amazonaws.com/275505252693/album-object-queue-real'

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def sleeper_agent(event, context):
    object_key = event["Records"][0]["s3"]["object"]["key"]
    logger.info(event)
    logger.info(object_key)
    stepfunctions = boto3.client('stepfunctions')
    state_machine_arn = 'arn:aws:states:eu-central-1:275505252693:stateMachine:MyStepFunction'
    input_data = {
        "object_key": object_key
    }
    input_json = json.dumps(input_data)

    stepfunctions.start_execution(
        stateMachineArn=state_machine_arn,
        input=input_json  # Provide input data as JSON string if needed
    )


    # # METADATA
    #
    # try:
    #     object_key = event["Records"][0]["s3"]["object"]["key"]
    #     logger.info(f'object_key: {object_key}')
    #     response = sqs.receive_message(
    #         QueueUrl=metadata_queue_url,
    #         MaxNumberOfMessages=10
    #     )
    #     for message in response["Messages"]:
    #         item_str = message['Body']
    #         logger.info(f'item_json: {item_str}')
    #         item = json.loads(item_str)
    #         if(object_key == item["object_key"]):
    #             metadata_table.put_item(Item=item)
    #             sqs.delete_message(
    #                 QueueUrl=metadata_queue_url,
    #                 ReceiptHandle=message["ReceiptHandle"]
    #             )
    #             logger.info('deleted message?')
    #
    #
    # except Exception as exp:
    #     exception_type, exception_value, exception_traceback = sys.exc_info()
    #     traceback_string = traceback.format_exception(exception_type, exception_value, exception_traceback)
    #     err_msg = json.dumps({
    #     "errorType": exception_type.__name__,
    #     "errorMessage": str(exception_value),
    #     "stackTrace": traceback_string})
    #
    #     logger.error(err_msg)
    #
    #
    # # ALBUM OBJECT
    # try:
    #     object_key = event["Records"][0]["s3"]["object"]["key"]
    #     logger.info(f'object_key: {object_key}')
    #     response = sqs.receive_message(
    #         QueueUrl=album_object_queue_url,
    #         MaxNumberOfMessages=10
    #     )
    #     for message in response["Messages"]:
    #         item_str = message['Body']
    #         logger.info(f'item_json: {item_str}')
    #         item = json.loads(item_str)
    #         if(object_key == item["object_key"]):
    #             album_object_table.put_item(Item=item)
    #             sqs.delete_message(
    #                 QueueUrl=album_object_queue_url,
    #                 ReceiptHandle=message["ReceiptHandle"]
    #             )
    #             logger.info('deleted message?')
    #
    #
    # except Exception as exp:
    #     exception_type, exception_value, exception_traceback = sys.exc_info()
    #     traceback_string = traceback.format_exception(exception_type, exception_value, exception_traceback)
    #     err_msg = json.dumps({
    #     "errorType": exception_type.__name__,
    #     "errorMessage": str(exception_value),
    #     "stackTrace": traceback_string})
    #
    #     logger.error(err_msg)


