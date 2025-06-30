import boto3

def lambda_handler(event, context):
    instance_id = event.get('InstanceId')
    if not instance_id:
        return {'error': 'Missing InstanceId'}

    ssm = boto3.client('ssm')

    try:
        response = ssm.send_command(
            InstanceIds=[instance_id],
            DocumentName="grow-volume",  # or "AWS-RunShellScript" with inline commands
            Parameters={
                'commands': [
                    'sudo growpart /dev/nvme0n1 1',
                    'sudo xfs_growfs /'
                ]
            },
            TimeoutSeconds=60
        )
        return {'message': 'Grow command sent via SSM', 'response': response}
    except Exception as e:
        return {'error': str(e)}