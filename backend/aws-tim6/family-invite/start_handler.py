import json
import boto3

stepfunctions = boto3.client('stepfunctions')
state_machine_arn = 'arn:aws:states:eu-central-1:275505252693:stateMachine:InviteStateMachine'


def start_handler(event, context):
    if 'requestContext' in event and 'authorizer' in event['requestContext']:
        user_info = event['requestContext']['authorizer']['claims']
        inviter = user_info['preferred_username']

        try:
            # dynamo db
            event_body = json.loads(event["body"])
            invitee = event_body.get("invitee_email")
            invitee_username = event_body.get("invitee_username")
            type_ = event_body.get("type")

            state_machine_input = {
                "inviter": inviter,
                "invitee": invitee,
                "invitee_username": invitee_username,
                "otherData": "other values",
                "type": type_
            }

            execution_response = stepfunctions.start_execution(
                stateMachineArn=state_machine_arn,
                input=json.dumps(state_machine_input)
            )

            response = {
                "statusCode": 200,
                "body": json.dumps({
                    "message": "Lambda function executed successfully",
                    "stateMachineResult": execution_response
                })
            }

            return response


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
    code = event['statusCode']
    body = event['body']
    # TODO implement
    return {
        'statusCode': code,
        'body': body
    }
