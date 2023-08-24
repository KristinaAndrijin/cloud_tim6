import json
import boto3


dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('userFiles')
client = boto3.client('cognito-idp')
user_pool_id = 'eu-central-1_N333IcKgF'



def remove_access_to_file_from_user(event, context):
    # print('eee')
    if 'requestContext' in event and 'authorizer' in event['requestContext']:
        user_info = event['requestContext']['authorizer']['claims']
        owner = user_info['preferred_username']
        # print('owner')
        try:
            # dynamo db
            event_body = json.loads(event["body"])
            file_key = event_body.get("file_key")
            username = event_body.get("username")
            # print(file_key, username)
            all_users = get_users()
            # print(all_users)
            if username not in all_users:
                # print('tu je')
                body = {
                    "message": "User doesn't exist"
                }
                return {
                    'statusCode': 400,
                    'body': json.dumps(body)
                }

            response = table.get_item(
                Key={
                    'username': username,
                    'file_key': file_key
                }
            )

            if 'Item' in response:
                
                # dynamo
                response = table.delete_item(
                    Key={
                        'username': username,
                        'file_key': file_key
                    }
                )

                if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                    body = {
                        "message": "Successful removal of access to file " + file_key,
                        "response": str(response)
                    }
                    return {"statusCode": 200, "body": json.dumps(body)}
                else:
                    body = {
                        "message": "Item wasn't deleted!",
                        "response": str(response)
                    }
                    return {"statusCode": 400, "body": json.dumps(body)}
            else:
                body = {
                    "message": "Item NOT found, user " + username + " does not access to file " + file_key,
                }
                return {"statusCode": 404, "body": json.dumps(body)}

        except dynamodb.meta.client.exceptions.ConditionalCheckFailedException:
            body = {
                "message": "Item already exists"
            }
            return {
                'statusCode': 400,
                'body': json.dumps(body)
            }
        except Exception as e:
            return {
                "statusCode": 400,
                "body": f"Error occurred: {str(e)}"
            }

    else:
        body = {
            "message": "Missing token",
        }
        return {"statusCode": 401, "body": json.dumps(body)}
    
    
def get_users():
    # print('hej')
    users_ret = []
    response = client.list_users(
        UserPoolId=user_pool_id
    )
    users = response['Users']
    for user in users:
        attributes = user['Attributes']
        for att in attributes:
            name = att['Name']
            # print('name', name)
            value = att['Value']
            # print('value', value)
            if (name == 'preferred_username'):
                users_ret.append(value)
                # print(users_ret)
    # print(users_ret)
    return users_ret
