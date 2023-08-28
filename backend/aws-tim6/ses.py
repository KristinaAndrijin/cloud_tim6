import json
import boto3

ses_client = boto3.client("ses")

code = 200
error = ""

def send_email(event, context):
    
    sender_email = "aws.tim6@gmail.com"
    recipient_email = "aws.tim6@gmail.com"
    subject = "Invitation to AWS TIM6"
    body = "Hello from the app!"
    
    try:
        response = ses_client.send_email(
            Source=sender_email,
            Destination={"ToAddresses": [recipient_email]},
            Message={"Subject": {"Data": subject}, "Body": {"Text": {"Data": body}}},
        )
        error = response
        code = 200
    except Exception as e:
        error = str(e)
        code = 500
        
    body = {
        "message": error,
        "input": event,
    }

    return {"statusCode": code, "body": json.dumps(body)}


def verify_identity(event, context):
    # Specify the identity to verify (email address or domain)
    identity_to_verify = 'andrijinkristina@gmail.com'  # Replace with the identity you want to verify

    try:
        # Verify the identity
        response = ses_client.verify_email_identity(EmailAddress=identity_to_verify)
        print(f"Verification initiated for {identity_to_verify}: {response}")
        return {
            'statusCode': 200,
            'body': json.dumps('Hello from Lambda!')
        }

    except Exception as e:
        print(f"Verification failed for {identity_to_verify}: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps('Bye from Lambda!')
        }