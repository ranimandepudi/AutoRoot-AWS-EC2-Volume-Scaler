import boto3
import time

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    volume_id = event['VolumeId']

    # Get current size
    volume = ec2.describe_volumes(VolumeIds=[volume_id])['Volumes'][0]
    current_size = volume['Size']
    new_size = int(current_size * 1.2)

    ec2.modify_volume(VolumeId=volume_id, Size=new_size)

    # Wait until modification state becomes 'optimizing' or 'completed'
    while True:
        vol_mod = ec2.describe_volumes_modifications(VolumeIds=[volume_id])['VolumesModifications'][0]
        if vol_mod['ModificationState'] in ['optimizing', 'completed']:
            break
        time.sleep(5)

    return {'message': f'Volume resized to {new_size} GB'}