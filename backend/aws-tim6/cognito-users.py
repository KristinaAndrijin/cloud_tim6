import json
import boto3

client = boto3.client('cognito-idp')
user_pool_id = 'eu-central-1_JTv6FBTKX'
user_client_id = '4n07bpdu5h012ali6g0nv8r6e7'

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
    
    
def confirm_user(event, context):
    try:
        response = client.admin_confirm_sign_up(
            UserPoolId=user_pool_id,
            Username="kristinaproba"
        )
        body = {
            "message": response,
            "input": event,
        }
        return {"statusCode": 200, "body": json.dumps(body)}
    except Exception as e:
        return {"statusCode": 500, "body": str(e)}
    
    
def delete_user(event, context):
    try:
        response = client.admin_delete_user(
            UserPoolId=user_pool_id,
            Username="kristinaproba"
        )
        body = {
            "message": response,
            "input": event,
        }
        return {"statusCode": 200, "body": json.dumps(body)}
    except Exception as e:
        return {"statusCode": 500, "body": str(e)}



def login(event, context):
    event_body = json.loads(event["body"])
    username = event_body.get("username")
    password = event_body.get("password")
    try:
        response = client.initiate_auth(
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': username,
                'PASSWORD': password
            },
            ClientId=user_client_id
        )
        return {
            'statusCode': 200,
            'body': 'User login successful'
        }
    except client.exceptions.NotAuthorizedException:
        return {
            'statusCode': 401,
            'body': 'Invalid credentials'
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f'Login failed: {str(e)}'
        }
    # return {
    #     'statusCode': 200,
    #     'body': json.dumps('Hello from Lambda!')
    # }

def signup(event, context):
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }