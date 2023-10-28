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
    # Extract the 'name' from the API event
    name = event.get('queryStringParameters', {}).get('name', 'defaultName')

    # Check if the object with the name already exists
    if object_exists(FLAGS_BUCKET, f'{name}.txt'):
        return {
            'statusCode': 409, # 409 Conflict
            'body': json.dumps({'message': f'File {name}.txt already exists in S3. Please modify the existing file or choose a different name to avoid naming conflicts.'})
        }

    # Create an S3 object with the name
    s3.put_object(
        Bucket=FLAGS_BUCKET,
        Key=f'{name}.txt',
        Body=json.dumps({'message': f'File created for {name}'})
    )

    # Response for API Gateway
    return {
        'statusCode': 200,
        'body': json.dumps({'message': f'Successfully created file for {name} in S3.'})
    }
