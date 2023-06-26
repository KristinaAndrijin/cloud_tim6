import json
import boto3


dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('invitations')

ses_client = boto3.client("ses")


def post_invitation(event, context):
    if 'requestContext' in event and 'authorizer' in event['requestContext']:
        user_info = event['requestContext']['authorizer']['claims']
        inviter_username = user_info['preferred_username']
        inviter_email = user_info['email']
        try:
            # dynamo db
            event_body = json.loads(event["body"])
            email = event_body.get("email")
            if (email == inviter_email):
                body = {
                    "message": "You cannot invite yourself :P"
                }
                return {
                    'statusCode': 400,
                    'body': json.dumps(body)
                }
            item = {
                'inviter': inviter_username,
                'invitee': email,
                'status': 'pending'
            }
            condition_expression = 'attribute_not_exists(inviter) AND attribute_not_exists(invitee)'
            table.put_item(Item=item, ConditionExpression=condition_expression)
            
            
            #ses
            sender_email = "aws.tim6@gmail.com"
            # recipient_email = email 
            recipient_email = "aws.tim6@gmail.com" #currently_hardcoded
            subject = "Invitation to AWS TIM6"
            message_body = "You're invited to our app by " + inviter_email +"! In order to accept invitation, click here: *neki link* and register!"
            response = ses_client.send_email(
                Source=sender_email,
                Destination={"ToAddresses": [recipient_email]},
                Message={"Subject": {"Data": subject}, "Body": {"Text": {"Data": message_body}}},
            )
            
            body = {
                "message": "Successfully invited person!",
                "inviter": inviter_username,
                "invitee": email
            }
            return {"statusCode": 200, "body": json.dumps(body)}
        except dynamodb.meta.client.exceptions.ConditionalCheckFailedException:
            body = {
                "message": "Item already exists"
            }
            return {
                'statusCode': 400,
                'body': json.dumps(body)
            }
        except Exception as e:
            return {"statusCode": 500, "body": str(e)}
        
    else:
        body = {
            "message": "Missing parameters",
        }
        return {"statusCode": 404, "body": json.dumps(body)}