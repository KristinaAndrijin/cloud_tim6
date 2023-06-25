import json
import boto3

client = boto3.client('cognito-idp')
user_pool_id = 'eu-central-1_JTv6FBTKX'

def get_users(event, context):
    try:
        mess = ""
        response = client.list_users(
            UserPoolId=user_pool_id
        )
        users = response['Users']
        for user in users:
            attributes = user['Attributes']
            for att in attributes:
                name = att['Name']
                value = att['Value']
                if (name == 'preferred_username'):
                    mess += value + ", "
        body = {
            "message": mess,
            "input": event,
        }
        return {"statusCode": 200, "body": json.dumps(body)}
    except Exception as e:
        return {"statusCode": 500, "body": str(e)}