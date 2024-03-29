import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('invitations')
table_userAlbum = dynamodb.Table('userAlbum')
table_userFiles = dynamodb.Table('userFiles')
table_albumObject = dynamodb.Table('albumObject')

ses_client = boto3.client("ses")

client = boto3.client('cognito-idp')
user_pool_id = 'eu-central-1_N333IcKgF'


def confirm_invite(event, context):
    # if 'requestContext' in event and 'authorizer' in event['requestContext']:
    # user_info = event['requestContext']['authorizer']['claims']
    # inviter = user_info['preferred_username']
    try:
        # dynamo db
        print('hello confirm')
        # print(event)
        event_body = event
        # print(event_body)
        inviter = event_body.get('inviter')
        invitee = event_body.get("invitee")

        print(inviter, invitee)

        response = table.get_item(
            Key={
                'inviter': inviter,
                'invitee': invitee
            }
        )

        if 'Item' in response and response['Item']['status'] == 'accepted':
            # user pool
            invitee_username = event_body.get("invitee_username")
            response = client.admin_confirm_sign_up(
                UserPoolId=user_pool_id,
                Username=invitee_username
            )

            # ses
            sender_email = "aws.tim6@gmail.com"
            recipient_email = invitee
            # recipient_email = "aws.tim6@gmail.com"  # currently_hardcoded
            subject = "Invitation to AWS TIM6"
            message_body = "Hello " + invitee_username + "! Your account is verified!! You can now login and use AWS TIM6 app as you wish! http://localhost:4200/"
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

            give_permissions(invitee_username, inviter)

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
    # else:
    #     body = {
    #         "message": "Missing token",
    #     }
    #     return {"statusCode": 401, "body": json.dumps(body)}


def give_permissions(invitee, inviter):
    # album
    response = table_userAlbum.scan()
    items = response['Items']
    while 'LastEvaluatedKey' in response:
        response = table_userAlbum.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        items.extend(response['Items'])
    albums = []
    for item in items:
        if item['username'] == inviter:
            albums.append(item['album_key'])
    for album in albums:
        item = {
            'username': invitee,
            'album_key': album
        }
        condition_expression = 'attribute_not_exists(username) AND attribute_not_exists(album_key)'
        table_userAlbum.put_item(Item=item, ConditionExpression=condition_expression)

    # get files
    response = table_albumObject.scan()
    items = response['Items']
    while 'LastEvaluatedKey' in response:
        response = table_albumObject.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        items.extend(response['Items'])
    files = []
    for item in items:
        if item['album_key'] == inviter:
            files.append(item['object_key'])

    # enter files
    for file in files:
        item = {
            'username': invitee,
            'file_key': file
        }
        condition_expression = 'attribute_not_exists(username) AND attribute_not_exists(album_key)'
        table_userFiles.put_item(Item=item, ConditionExpression=condition_expression)


