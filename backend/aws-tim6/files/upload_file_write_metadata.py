import json
import boto3

dynamodb = boto3.resource('dynamodb')

def write_metadata_upload(event, context):
    try:
        metadata_table = dynamodb.Table('filesMetadata')

        item = {
            'object_key': "xd",
            'name': "xd",
            'type': "xd",
            'size': "xd",
            'upload_date': "datummm",
            'tags': "ijoooj,xd,fuf",
            'description': "asdsa",
        }

        response = metadata_table.put_item(
            Item=item,
            ConditionExpression='attribute_not_exists(object_key)'
        )

        body = {
            "message": "Metadata added successfully",
        }
        return {"statusCode": 200, "body": json.dumps(body)}



    except Exception as e:

        body = {
            "message": str(e),
        }
        return {"statusCode": 500, "body": json.dumps(body)}
