import json
import boto3

# Create an SNS client
sns_client = boto3.client('sns')

# Specify the SNS topic ARN
topic_arn = 'arn:aws:sns:eu-central-1:275505252693:ProbaTopic'

# Specify the message to publish
message = 'Hello pls radi!'

error = "jej"
code = 200


def publish(event, context):
    try:
        response = sns_client.publish(
            TopicArn=topic_arn,
            Message=message
        )
        error = response
        code = 200
    except Exception as e:
        error = e
        code = 500
        
    body = {
        "message": error,
        "input": event,
    }

    return {"statusCode": code, "body": json.dumps(body)}


endpoint = 'andrijinkristina@gmail.com'
protocol = 'email'


def subscribe(event, context):
    try:
        response = sns_client.subscribe(
            TopicArn=topic_arn,
            Protocol=protocol,
            Endpoint=endpoint
        )
        error = "slay"
        code = 200
    except Exception as e:
        error = str(e)
        code = 500
        
    body = {
        "message": error,
        "input": event,
    }

    return {"statusCode": code, "body": json.dumps(body)}
