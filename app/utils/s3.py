import boto3
from botocore.exceptions import ClientError

s3_client = boto3.client(
    's3',
    endpoint_url='http://localstack:4566',
    region_name='us-east-1'
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
