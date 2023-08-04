import json
import boto3
from constants import *


dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('invitations')

ses_client = boto3.client("ses")

client = boto3.client('cognito-idp')


def confirm_invite(event, context):
    if 'requestContext' in event and 'authorizer' in event['requestContext']:
        user_info = event['requestContext']['authorizer']['claims']
        inviter = user_info['preferred_username']
        try:
            # dynamo db
            event_body = json.loads(event["body"])
            invitee = event_body.get("invitee_email")
            
            response = table.get_item(
                Key={
                    'inviter': inviter,
                    'invitee': invitee
                }
            )

            if 'Item' in response and response['Item']['status'] == 'accepted':
                #user pool
                invitee_username = event_body.get("invitee_username")
                response = client.admin_confirm_sign_up(
                    UserPoolId=user_pool_id,
                    Username=invitee_username
                )
                
                # ses
                sender_email = "aws.tim6@gmail.com"
                # recipient_email = event_body.get("inviter_email")
                recipient_email = "aws.tim6@gmail.com" #currently_hardcoded
                subject = "Invitation to AWS TIM6"
                message_body = "Hello " + invitee_username +"! Your account is verified!! You can now login and use AWS TIM6 app as you wish! http://localhost:4200/"
                response = ses_client.send_email(
                    Source=sender_email,
                    Destination={"ToAddresses": [recipient_email]},
                    Message={"Subject": {"Data": subject}, "Body": {"Text": {"Data": message_body}}},
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
                        "message": "Successful conformation of identity",
                        "response": str(response)
                    }
                    return {"statusCode": 200, "body": json.dumps(body)}
                else:
                    body = {
                        "message": "Item wasnt deleted!",
                        "response": str(response)
                    }
                    return {"statusCode": 400, "body": json.dumps(body)}
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
    else:
        body = {
            "message": "Missing token",
        }
        return {"statusCode": 401, "body": json.dumps(body)}