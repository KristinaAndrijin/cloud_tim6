import json
import boto3

dynamodb = boto3.resource('dynamodb')
def write_metadata_upload(event, context):

    try:
        metadata_table = dynamodb.Table('filesMetadata')

        item = {
            'object_key': {'S': object_key},
            'name': {'S': dir_name},
            'type': {'S': dir_type},
            'size': {'S': dir_size},
            'upload_date': {'N': str(modification_time)},
            'tags': {'N': "xd"},
            'description': {'N': "asdsa"},
        }

        response = db.put_item(
            TableName='files_metadata',
            Item=item,
            ConditionExpression='attribute_not_exists(object_key)'
        )


    except:
        pass

