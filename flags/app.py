import json

# curl --location 'https://swd0o1s1ae.execute-api.us-east-1.amazonaws.com/Prod/flags/'

def lambda_handler(event, context):
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Changed"
        }),
    }
