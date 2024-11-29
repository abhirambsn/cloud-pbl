import boto3
from botocore.exceptions import ClientError

print("Setting up S3 Client")

s3_client = boto3.client(
    's3',
    endpoint_url='http://localhost:4566',
    region_name='us-east-1',
    aws_access_key_id='test',
    aws_secret_access_key='test'
)

def upload_to_s3(file, bucket_name):
    try:
        s3_client.create_bucket(Bucket=bucket_name)
    except ClientError as e:
        if e.response['Error']['Code'] != 'BucketAlreadyOwnedByYou':
            raise e
    s3_client.upload_fileobj(file, bucket_name, file.filename)

def list_s3_objects(bucket_name):
    try:
        response = s3_client.list_objects_v2(Bucket=bucket_name)
        return [obj['Key'] for obj in response.get('Contents', [])]
    except ClientError as e:
        return []

def get_s3_object(key, bucket_name):
    try:
        return s3_client.get_object(Bucket=bucket_name, Key=key)
    except ClientError as e:
        return None