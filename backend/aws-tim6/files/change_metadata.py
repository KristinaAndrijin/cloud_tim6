import json
import boto3
from decimal import Decimal

dynamodb = boto3.client('dynamodb')

def change_metadata(event, context):
    try:
        request_body = json.loads(event['body'])
        obj_key = request_body['obj_key']
        description = request_body['description']
        tags = request_body['tags']

        response = dynamodb.update_item(
            TableName='filesMetadata',
            Key={
                'object_key': {'S': obj_key}
            },
            UpdateExpression='SET #desc = :descVal, #tags = :tagsVal',
            ExpressionAttributeNames={
                '#desc': 'description',
                '#tags': 'tags'
            },
            ExpressionAttributeValues={
                ':descVal': {'S': description},
                ':tagsVal': {'S': tags}
            }
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
