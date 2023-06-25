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