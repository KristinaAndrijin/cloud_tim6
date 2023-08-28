import json
import boto3

dynamodb = boto3.client('dynamodb')


def add_to_album(event, context):
    try:
        request_body = json.loads(event['body'])
        obj_key_from_front = request_body['object_key']
        album_key_from_front = request_body['album_key']
        upload_date_from_front = request_body['upload_date']

        print("upload date", upload_date_from_front)

        response = dynamodb.scan(
            TableName='albumObject',
            FilterExpression='album_key = :album_key and object_key = :object_key',
            ExpressionAttributeValues={
                ':album_key': {'S': album_key_from_front},
                ':object_key': {'S': obj_key_from_front}
            }
        )

        if len(response["Items"]) > 0:
            body = {
                "message": "File is already in album",
            }
            return {"statusCode": 404, "body": json.dumps(body)}
        else:

            item_to_store = {
                "album_key": {'S': album_key_from_front},
                "object_key": {'S': obj_key_from_front},
                "upload_date": {'S': upload_date_from_front}
            }

            response = dynamodb.put_item(
                TableName='albumObject',
                Item=item_to_store
            )

        return {
            "statusCode": 200,
            "body": json.dumps(response)
        }

    except Exception as e:
        body = {
            "message": str(e),
        }
        return {"statusCode": 500, "body": json.dumps(body)}
