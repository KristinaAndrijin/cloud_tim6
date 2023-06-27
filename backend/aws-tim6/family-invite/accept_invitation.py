import json
import boto3


dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('invitations')

ses_client = boto3.client("ses")


client = boto3.client('cognito-idp')
user_pool_id = 'eu-central-1_JTv6FBTKX'


def accept_invitation(event, context):
    event_body = json.loads(event["body"])
    try:
        inviter = event_body.get("inviter")
        invitee = event_body.get("invitee")
        key = {
            'inviter': inviter,
            'invitee': invitee
        }

        update_expression = 'SET #statusAttr = :newStatus'
        expression_attribute_names = {'#statusAttr': 'status'}
        expression_attribute_values = {':newStatus': 'accepted'}

        table.update_item(
            Key=key,
            UpdateExpression=update_expression,
            ExpressionAttributeNames=expression_attribute_names,
            ExpressionAttributeValues=expression_attribute_values,
            ConditionExpression='attribute_exists(inviter) AND attribute_exists(invitee)'
        )
        body = {
                "message": "Successfully accepted invite!"
        }
        
        invitee_username = event_body.get("invitee_username")
        #ses
        sender_email = "aws.tim6@gmail.com"
        # recipient_email = event_body.get("inviter_email")
        recipient_email = "aws.tim6@gmail.com" #currently_hardcoded
        subject = "Invitation to AWS TIM6"
        message_body = "User " + invitee + " has accepted your invitation to join the app! Please confirm that you sent the invitation here: http://localhost:4200/resolve-invitation?inviter="+inviter+"&invitee_email="+invitee+"&invitee_username="+invitee_username;
        response = ses_client.send_email(
            Source=sender_email,
            Destination={"ToAddresses": [recipient_email]},
            Message={"Subject": {"Data": subject}, "Body": {"Text": {"Data": message_body}}},
        )
        
        return {"statusCode": 200, "body": json.dumps(body)}
    
    except dynamodb.meta.client.exceptions.ConditionalCheckFailedException:
        invitee_username = event_body.get("invitee_username")
        response = client.admin_delete_user(
            UserPoolId=user_pool_id,
            Username=invitee_username
        )
        body = {
            "message": "You were not invited ):("
        }
        return {
            'statusCode': 400,
            'body': json.dumps(body)
        }
    except Exception as e:
        invitee_username = event_body.get("invitee_username")
        response = client.admin_delete_user(
            UserPoolId=user_pool_id,
            Username=invitee_username
        )
        body = {
            "message": str(e)
        }
        return {
            'statusCode': 400,
            'body': json.dumps(body)
        }