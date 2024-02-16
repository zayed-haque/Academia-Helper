import json
from boto3 import client as botoClient


def get_credentials():
    s3 = botoClient('s3')
    response = s3.get_object(Bucket='academia-credentials', Key='credentials.json')
    userdata = json.loads(response['Body'].read())
    return json.loads(response['Body'].read())


def invoke_slave(userdata):
    successful_users = []
    failed_users = []
    for user in userdata:
        try:
            if 'username' not in user or 'password' not in user:
                raise Exception("Invalid Credentials")
            payload = {
                "username": user['username'],
                "password": user['password']
            }
            lambda_client = botoClient('lambda')
            lambda_client.invoke(FunctionName="Academia_Attendance", InvocationType="Event", Payload=json.dumps(payload))
            successful_users.append(user['username'])
        except Exception as e:
            failed_users.append(user['username'])
            continue
    return {
        "successful_users": successful_users,
        "failed_users": failed_users
    }