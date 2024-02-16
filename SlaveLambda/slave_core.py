from logger import LogType, log
from slave_utils import get_attendance
import json

TAG = "Academia_Attendance_Slave_Lambda"


def lambda_handler(event, context):
    # TODO implement
    username = event['username']
    password = event['password']
    try:
        attendance = get_attendance(username, password)
        log(TAG, LogType.INFO, "Data retrieved for " + str(username))
    except Exception as e:
        log(TAG, LogType.ERROR, "Error fetching data for " + str(username) + " : " + str(e))
        return {
            'statusCode': 500,
            'body': json.dumps(f"Slave Lambda Error: {str(e)}")
        }
    return {
        'statusCode': 200,
        'body': json.dumps(attendance)
    }