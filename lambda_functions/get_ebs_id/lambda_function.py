import boto3

def lambda_handler(event, context):
    ec2_client = boto3.client('ec2')
    instance_id = event.get('InstanceId')
    if not instance_id:
        raise ValueError("Missing InstanceId in input")

    response = ec2_client.describe_instances(InstanceIds=[instance_id])
    instance = response['Reservations'][0]['Instances'][0]

    for dev in instance['BlockDeviceMappings']:
        if dev['DeviceName'] == instance['RootDeviceName']:
            return {'VolumeId': dev['Ebs']['VolumeId']}

    raise Exception("Root volume not found")