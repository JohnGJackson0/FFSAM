import json
import boto3
import os

# curl --location 'https://swd0o1s1ae.execute-api.us-east-1.amazonaws.com/Prod/flags/?name=example_flag'

s3 = boto3.client('s3')
FLAGS_BUCKET = os.environ['FLAGS_BUCKET']

def object_exists(bucket, key):
    """Check if an object exists in the S3 bucket."""
    try:
        s3.head_object(Bucket=bucket, Key=key)
        return True
    except s3.exceptions.ClientError as e:
        if e.response['Error']['Code'] == '404':
            return False
        else:
            raise

def lambda_handler(event, context):
    name = event.get('queryStringParameters', {}).get('name', 'defaultName')
    if object_exists(FLAGS_BUCKET, f'{name}.txt'):
        return {
            'statusCode': 409,
            'body': json.dumps({'message': f'File {name}.txt already exists in S3. Please modify the existing file or choose a different name to avoid naming conflicts.'})
        }
    s3.put_object(
        Bucket=FLAGS_BUCKET,
        Key=f'{name}.txt',
        Body=json.dumps({'flag': False})
    )
    return {
        'statusCode': 200,
        'body': json.dumps({'message': f'Successfully created file for {name} in S3.'})
    }
