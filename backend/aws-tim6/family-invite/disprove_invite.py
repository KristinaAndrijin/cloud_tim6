import json
import boto3


dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('invitations')
ses_client = boto3.client("ses")
user_pool_id = 'eu-central-1_N333IcKgF'
client = boto3.client('cognito-idp')


def disprove_invite(event, context):
    # if 'requestContext' in event and 'authorizer' in event['requestContext']:
    # user_info = event['requestContext']['authorizer']['claims']
    # inviter = user_info['preferred_username']
    try:
        # dynamo db
        event_body = event
        inviter = event_body.get('inviter')
        invitee = event_body.get("invitee_email")

        response = table.get_item(
            Key={
                'inviter': inviter,
                'invitee': invitee
            }
        )

        if 'Item' in response and response['Item']['status'] == 'accepted':
            invitee_username = event_body.get("invitee_username")
            response = client.admin_delete_user(
                UserPoolId=user_pool_id,
                Username=invitee_username
            )

            # dynamo
            response = table.delete_item(
                Key={
                    'inviter': inviter,
                    'invitee': invitee
                }
            )

            if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                body = {
                    "message": "Successful disploval of identity",
                    "response": str(response)
                }
                return {"statusCode": 200, "body": json.dumps(body)}
            else:
                body = {
                    "message": "Item wasnt deleted!",
                    "response": str(response)
                }
                return {"statusCode": 400, "body": json.dumps(body)}

            # body = {
            #     "message": "User is deleted",
            #     "response": str(response)
            # }
            # return {"statusCode": 200, "body": json.dumps(body)}
        elif 'Item' in response and response['Item']['status'] != 'accepted':
            body = {
                "message": "This invitation wasn't verified by invited user",
                "response": str(response)
            }
            return {"statusCode": 200, "body": json.dumps(body)}
        else:
            body = {
                "message": "Item NOT found, this invitation wasn't sent!",
            }
            return {"statusCode": 404, "body": json.dumps(body)}

    except Exception as e:
        body = {
            "message": str(e),
        }
        return {"statusCode": 500, "body": json.dumps(body)}
    # else:
    #     body = {
    #         "message": "Missing token",
    #     }
    #     return {"statusCode": 401, "body": json.dumps(body)}