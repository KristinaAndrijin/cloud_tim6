import json
import logging
import boto3

s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('filesMetadata')

sqs = boto3.client('sqs')
metadata_queue_url = 'https://sqs.eu-central-1.amazonaws.com/275505252693/metadata-queue'

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def write_metadata(event, context):
    print("pozzz")

    object_key = event.get("object_key").replace(" ", "+")
    response = sqs.receive_message(
        QueueUrl=metadata_queue_url,
        MaxNumberOfMessages=10
    )
    print(response)
    for message in response["Messages"]:
        item_str = message['Body']
        item = json.loads(item_str)
        item_ok = item["object_key"].replace(" ", "+")
        if object_key == item_ok:
            print("aaaaaa")

            if item["replaces"] is not None:
                if item["replaces"].replace(" ", "+") != item_ok:
                    replace_helper(item)
                    sqs.delete_message(
                        QueueUrl=metadata_queue_url,
                        ReceiptHandle=message["ReceiptHandle"]
                    )
            else:
                table.put_item(Item=item)
                sqs.delete_message(
                    QueueUrl=metadata_queue_url,
                    ReceiptHandle=message["ReceiptHandle"]
                )
                logger.info('deleted message?')
                break


def replace_helper(item):

    # ako se desi da novi fajl koji se uploaduje da "edit"uje prošli ima drugačije ime, onda mora da zameni sve pojave starog u tabelama
    print("počeo sammmmm")
    bucket_name = 'projekat6'
    metadata_table = 'filesMetadata'
    album_object_table = 'albumObject'
    user_files_table = 'userFiles'
    real_dynamodb = boto3.client('dynamodb')

    # zamena samog s3 objekta
    try:
        s3_client.delete_object(
            Bucket=bucket_name,
            Key=item["replaces"]
        )
        print('radi s3')
    except Exception as e:
        print('ne radi s3')
        print(e)
        return {
            "statusCode": 400,
            "body": f"Error occurred: {str(e)}"
        }

    # zamena u metadata
    try:
        real_dynamodb.delete_item(
            TableName=metadata_table,
            Key={"object_key": {"S": item["replaces"]}}
        )
    except Exception as e:
        print(e)
        print('ne radi metadata')
        return {
            "statusCode": 400,
            "body": f"Error occurred: {str(e)}"
        }

    try:
        table.put_item(Item=item)
    except Exception as e:
        print('ne radi upis metadata')
        return {
            "statusCode": 400,
            "body": f"Error occurred: {str(e)}"
        }

    # zamena u album object

    try:
        response = real_dynamodb.scan(
            TableName=album_object_table,
            Select='ALL_ATTRIBUTES',
            FilterExpression='object_key = :val',
            ExpressionAttributeValues={':val': {'S': item["replaces"]}}
        )
        for result in response["Items"]:
            key = {
                'album_key': result['album_key'],
                'object_key': result['object_key']
            }
            real_dynamodb.delete_item(
                TableName=album_object_table,
                Key=key
            )

            album_object_item = {
                'album_key': result['album_key'],
                'object_key': {'S': item["object_key"]},
                'upload_date': result['upload_date']

            }
            real_dynamodb.put_item(
                TableName=album_object_table,
                Item=album_object_item
            )

    except Exception as e:
        print('ne radi albumObject')
        print(e)
        return {
            "statusCode": 400,
            "body": f"Error occurred: {str(e)}"
        }







