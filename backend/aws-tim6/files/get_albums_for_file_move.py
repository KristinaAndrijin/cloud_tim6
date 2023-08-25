import json
import boto3

dynamodb = boto3.client('dynamodb')


def get_albums(event, context):
    try:
        user_info = event['requestContext']['authorizer']['claims']
        username = user_info['preferred_username']
        request_body = json.loads(event['body'])
        obj_key_from_front = request_body['object_key']

        if username != obj_key_from_front.split("/")[0]:
            body = {
                "message": "Error: Adding a file to an album that doesn't belong to the logged user.",
            }
            return {
                "statusCode": 404,
                "body": json.dumps(body)
            }

        #dobavi sve iz user album, sačuvaj samo one koji počinju sa username + username sam
        #procesom eliminacije skidaj sve one koji imaju object_key par 
        # Scan the entire DynamoDB table
        response_album_object = dynamodb.scan(
            TableName='albumObject',
        )

        response_user_album = dynamodb.scan(
            TableName='userAlbum',
        )

        albums_without_object = set()
        for item in response_user_album["Items"]:
            album_key = item['album_key']['S']
            username_db = item['username']['S']

            if album_key.split("/")[0] == username:
                albums_without_object.add(album_key)

        albums_without_object.add(username)

        print(response_album_object["Items"])
        for item in response_album_object['Items']:
            album_key = item['album_key']['S']
            object_key = item['object_key']['S']

            # print("album_key: "+album_key,"username:"+username, "starts:"+str(album_key.startswith(username)))
            # print("object_key: "+object_key + " obj_front: "+obj_key_from_front + " object_key != obj_key_from_front:" +str(object_key != obj_key_from_front))
            # print("ceo if: "+ str(album_key.startswith(username) and object_key != obj_key_from_front))
            if album_key.split("/")[0] == username and object_key == obj_key_from_front:
                print("izbacujeeem")
                if album_key in albums_without_object:
                    albums_without_object.remove(album_key)

        # Prepare a list of objects with album_name and owner
        result_list = []
        print(albums_without_object)
        for album in albums_without_object:

            result_list.append({
                "name": album,
                "owner": username
            })

        return {
            "statusCode": 200,
            "body": json.dumps(result_list)
        }

    except Exception as e:
        body = {
            "message": str(e),
        }
        return {"statusCode": 500, "body": json.dumps(body)}
