import boto3
import os
import json
s3 = boto3.client('s3')
#curl --location 'https://swd0o1s1ae.execute-api.us-east-1.amazonaws.com/Prod/flags/list'
def lambda_handler(event, context):
    bucket_name = os.environ['FLAGS_BUCKET']
    response = s3.list_objects_v2(Bucket=bucket_name)
    flags_data = {}
    for item in response.get('Contents', []):
        flag_name = item['Key']
        if flag_name.endswith('.txt'):
            flag_name = flag_name[:-4]
            content_response = s3.get_object(Bucket=bucket_name, Key=item['Key'])
            content = content_response['Body'].read().decode('utf-8')
            flag_value = json.loads(content).get('flag', False)
            flags_data[flag_name] = flag_value
    return {
        'statusCode': 200,
        'body': json.dumps(flags_data),
        'headers': {
            'Content-Type': 'application/json'
        }
    }
