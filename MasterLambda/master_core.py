# This is the master lambda function that is responsible for invoking the slave lambda function and getting the logs from it.
import json
from logger import LogType, log
from master_utils import get_credentials, invoke_slave

TAG = "Academia_Attendance_Master_Lambda"


def lambda_handler(event, context):
    # TODO implement
    try:
        userdata = get_credentials()
        user_logs = invoke_slave(userdata)
        log(TAG, LogType.INFO, "Job completed successfully. Logs: " + str(user_logs))
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f"Master Lambda Error: {str(e)}")
        }
    return {
        'statusCode': 200,
        'body': json.dumps(user_logs)
    }
