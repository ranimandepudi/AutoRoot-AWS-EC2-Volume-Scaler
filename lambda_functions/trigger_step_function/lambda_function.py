import boto3
import json

def lambda_handler(event, context):
    # Extract InstanceId from the CloudWatch Alarm event details
    detail = event.get('detail', {})
    config = detail.get('configuration', {})
    # Metric alarms include a metrics array with dimensions list
    instance_id = None
    for metric in config.get('metrics', []):
        for dim in metric.get('dimensions', []):
            if dim.get('name') == 'InstanceId':
                instance_id = dim.get('value')
                break
        if instance_id:
            break
    if not instance_id:
        raise KeyError('InstanceId not found in alarm event')
    client = boto3.client('stepfunctions')
    payload = {'InstanceId': instance_id}
    response = client.start_execution(
        stateMachineArn='arn:aws:states:REGION:ACCOUNT_ID:stateMachine:STEP_FUNCTION_NAME',
        input=json.dumps(payload)
    )
    return {
        'statusCode': 200,
        'body': f"Step Function started for {instance_id}: {response.get('executionArn')}"
    }