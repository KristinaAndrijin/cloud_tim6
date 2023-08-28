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

ses_client = boto3.client("ses")

client = boto3.client('cognito-idp')
user_pool_id = 'eu-central-1_N333IcKgF'


def write_metadata(event, context):
    print("pozzz")
    email =""

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
            print(object_key)
            user = object_key.split('/')[0]
            print(user)
            email = find_user(user)

            if item["replaces"] is not None:
                if item["replaces"].replace(" ", "+") != item_ok:
                    replace_helper(item, email)
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
                subject = "File uploaded"
                item_str = "name: " + str(item['name']) + "\n" \
                           + "type: " + str(item['type']) + "\n" \
                           + "size: " + str(item['size']) + "\n" \
                           + "upload date: " + str(item['upload_date']) + "\n" \
                           + "tags: " + str(item['tags']) + "\n" \
                           + "description: " + str(item['description']) + "\n"
                body = "File " + object_key + " has been successfully uploaded!\n" + item_str
                send_email(email, subject, body)
                logger.info('deleted message?')
                break


def replace_helper(item, email):

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
        print('item', item)
    except Exception as e:
        print('ne radi s3')
        print(e)
        subject = "Error"
        body = "There has been an error while uploading file :("
        send_email(email, subject, body)
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
        subject = "Error"
        body = "There has been an error while uploading file :("
        send_email(email, subject, body)
        return {
            "statusCode": 400,
            "body": f"Error occurred: {str(e)}"
        }

    try:
        table.put_item(Item=item)
    except Exception as e:
        print('ne radi upis metadata')
        subject = "Error"
        body = "There has been an error while uploading file :("
        send_email(email, subject, body)
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
        subject = "Error"
        body = "There has been an error while uploading file :("
        send_email(email, subject, body)
        return {
            "statusCode": 400,
            "body": f"Error occurred: {str(e)}"
        }

    # zamena u user files

    try:
        response = real_dynamodb.scan(
            TableName=user_files_table,
            Select='ALL_ATTRIBUTES',
            FilterExpression='file_key = :val',
            ExpressionAttributeValues={':val': {'S': item["replaces"]}}
        )
        for result in response["Items"]:
            key = {
                'username': result['username'],
                'file_key': result['file_key']
            }
            real_dynamodb.delete_item(
                TableName=user_files_table,
                Key=key
            )

            user_files_item = {
                'username': result['username'],
                'file_key': {'S': item["object_key"]},
            }
            real_dynamodb.put_item(
                TableName=user_files_table,
                Item=user_files_item
            )

        subject = "File successfully updated"
        item_str = "name: " + str(item['name']) +"\n"\
                   + "type: " + str(item['type']) +"\n"\
                   + "size: " + str(item['size']) +"\n" \
                   + "upload date: " + str(item['upload_date']) +"\n" \
                   + "tags: " + str(item['tags']) + "\n" \
                   + "description: " + str(item['description']) + "\n"

        body = "You have successfully updated  file " + item["replaces"] + " to " + item["object_key"] + ".\n" + item_str
        send_email(email, subject, body)

    except Exception as e:
        print('ne radi userFiles')
        print(e)
        subject = "Error"
        body = "There has been an error while uploading file :("
        send_email(email, subject, body)
        return {
            "statusCode": 400,
            "body": f"Error occurred: {str(e)}"
        }


def send_email(recipient_email, subject, body):
    sender_email = "aws.tim6@gmail.com"
    # body = "Hello from the app!"

    try:
        response = ses_client.send_email(
            Source=sender_email,
            Destination={"ToAddresses": [recipient_email]},
            Message={"Subject": {"Data": subject}, "Body": {"Text": {"Data": body}}},
        )
        error = response
        code = 200
    except Exception as e:
        error = str(e)
        code = 500

    body = {
        "message": error
    }

    return {"statusCode": code, "body": json.dumps(body)}



def find_user(username):
    email = ""
    user_ = None
    response = client.list_users(
        UserPoolId=user_pool_id
    )
    users = response['Users']
    for user in users:
        attributes = user['Attributes']
        for att in attributes:
            name = att['Name']
            value = att['Value']
            if (name == 'preferred_username' and value == username):
                user_ = user
                break

    attributes = user_['Attributes']
    for att in attributes:
        name = att['Name']
        value = att['Value']
        if (name == 'email'):
            email = value

    return email

