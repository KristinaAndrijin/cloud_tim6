import os

import boto3
from keys import *

username="djole"
session = boto3.Session(
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_access_key,
    region_name=region_name
)
def upload_object(s3_client, file_path, bucket_name):
    response = s3_client.list_objects(Bucket=bucket_name, Prefix=username+"/", Delimiter="/")
    if "Contents" in response.keys():
        object_key = username+"/"+'object' + str(len(response['Contents']) + 1)
    else:
        object_key = username+"/"+'object1'

    s3_client.upload_file(file_path, bucket_name, object_key)
    print ("objekat "+file_path+ " postavljen kao "+object_key)

def print_all_objects(s3_client, bucket_name):
    response = s3_client.list_objects(Bucket=bucket_name)
    try:
        for o in response['Contents']:
            print(f"\t{o['Key']}")
    except (KeyError):
        print(f"\tNo content in bucket")

def run_s3():

    s3_client = session.client('s3')
    bucket_name = 'projekat'

    response = s3_client.list_buckets()
    if bucket_name not in response['Buckets']:
        bucket = s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration = {'LocationConstraint': region_name})

    for dir in os.listdir("test_fajlovi"):
        upload_object(s3_client,"test_fajlovi/"+dir,bucket_name)

    # Delete object
    # print("=== Delete object from bucket ===")
    # s3_client.delete_objects(Bucket=bucket_name, Delete={'Objects': [{'Key': object_key}]})

    # Delete bucket
    # print("=== Delete bucket ===")
    # s3_resource = session.resource('s3')
    # bucket = s3_resource.Bucket(bucket_name)
    # bucket.objects.all().delete()
    # bucket.delete()


if __name__ == '__main__':
    run_s3()