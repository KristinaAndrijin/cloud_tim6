from flask import Blueprint, request, make_response
from flask_api import status
from keys import *
import re
import botocore
import datetime
import boto3
import os

upload_bp = Blueprint('upload', __name__)

session = boto3.Session(
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_access_key,
    region_name=region_name
)
db = session.client('dynamodb')
s3_client = session.client('s3')


def upload_object(s3_client, file_path, bucket_name, username):
    response = s3_client.list_objects(Bucket=bucket_name, Prefix=username + "/", Delimiter="/")
    if "Contents" in response.keys():
        object_key = username + "/" + 'object' + str(len(response['Contents']) + 1)
    else:
        object_key = username + "/" + 'object1'

    s3_client.upload_file(file_path, bucket_name, object_key)
    print("objekat " + file_path + " postavljen kao " + object_key)
    return bucket_name + "/" + object_key


def get_file_size(file_path, unit='mb'):
    file_size = os.path.getsize(file_path)
    exponents_map = {'bytes': 0, 'KB': 1, 'MB': 2, 'GB': 3}
    if unit not in exponents_map:
        raise ValueError("Must select from \
        ['bytes', 'KB', 'MB', 'GB']")
    else:
        size = file_size / 1024 ** exponents_map[unit]
        return round(size, 3)


@upload_bp.route('/upload', methods=['post'])
def run_s3():
    username = request.cookies.get('username')
    bucket_name = 'projekat21'
    found = False
    response = s3_client.list_buckets()
    buckets = response['Buckets']
    if len(buckets) == 0:
        bucket = s3_client.create_bucket(Bucket=bucket_name,
                                         CreateBucketConfiguration={'LocationConstraint': region_name})
        # return "Nema baketa, napravljen je"
    for bucket in buckets:
        if bucket['Name'] == bucket_name:
            found = True
            break
    if not found:
            bucket = s3_client.create_bucket(Bucket=bucket_name,
                                             CreateBucketConfiguration={'LocationConstraint': region_name})

    for dir in os.listdir("./test_fajlovi"):
        dir_name = dir.split(".")[0]  # naziv datoteke
        dir_type = dir.split(".")[1]  # tip datoteke //a sta ako ima nesto kao qmd_1304.tar.gz ?

        size_arg = "KB"
        dir_size = str(get_file_size("test_fajlovi/" + dir, size_arg)) + " " + size_arg  # velicina fajla

        modification_time = os.path.getmtime("test_fajlovi/" + dir)  # vreme poslednje izmene
        modification_date = datetime.datetime.fromtimestamp(modification_time)

        creation_time = os.path.getctime("test_fajlovi/" + dir)  # vreme kreiranja
        creation_date = datetime.datetime.fromtimestamp(creation_time)

        object_key = upload_object(s3_client, "test_fajlovi/" + dir, bucket_name, username)

        item = {
            'object_key': {'S': object_key},
            'dir_name': {'S': dir_name},
            'dir_type': {'S': dir_type},
            'dir_size': {'S': dir_size},
            'modification_date': {'N': str(modification_time)},
            'creation_date': {'N': str(creation_time)}
        }

        try:
            response = db.put_item(
                TableName='files_metadata',
                Item=item,
                ConditionExpression='attribute_not_exists(object_key)'
            )
            # return "Successful"
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
                return "File " + object_key + " already exists in this folder", status.HTTP_400_BAD_REQUEST
            else:
                return "Error:" + str(e), status.HTTP_500_INTERNAL_SERVER_ERROR

    return "Successful"