# Demo Instructions

This document walks you through deploying and testing the Root Volume Expansion automation.

## 1. Fill in ARNs and IDs
  - Open `cloudformation/RootGuardAlarm.yaml` and set the `EC2Instance` parameter to your target instance ID or logical resource.
  - Provide the EventBridge rule ARN (`RootGuardEventRuleARN`) that will receive the alarm.
  - In `lambda_functions/trigger_step_function/lambda_function.py`, replace the placeholder `stateMachineArn` with your Step Function ARN.
  - In `eventbridge_rule/eventbridge_rule.json`, set the target Lambda ARN for your trigger function.

## 2. Deploy
  - Package and deploy your AWS SAM or CloudFormation templates:
    ```bash
    aws cloudformation deploy \
      --template-file cloudformation/RootGuardAlarm.yaml \
      --stack-name RootGuardAlarmStack \
      --parameter-overrides EC2Instance=<your-instance-id> RootGuardEventRuleARN=<your-eventbridge-rule-arn>
    ```
  - Ensure your Lambdas and Step Function are deployed and the EventBridge rule is active.

## 3. Simulate high disk usage
  - Copy `demo_scripts/disk_eater.sh` to your EC2 instance:
    ```bash
    scp demo_scripts/disk_eater.sh ec2-user@<your-instance>:/home/ec2-user/
    ssh ec2-user@<your-instance>
    chmod +x disk_eater.sh
    ./disk_eater.sh
    ```
  - The script will fill `/tmp` until root volume usage ≥95%.

## 4. Observe the automation
  - In the AWS Console:
    1. Watch the CloudWatch Alarm transition to ALARM.
    2. Check the EventBridge rule metrics to see it invoked `trigger_step_function`.
    3. Open Step Functions > Executions to follow the state machine progress.
    4. Monitor SSM > Run Command history to view the `grow-volume` document execution.
    5. Verify the volume size and filesystem growth with `df -h` on the instance.

# Appendix: Testing & Notifications

- **SNS/Slack Alerts**: Attach an SNS topic to your CloudWatch Alarm's `AlarmActions` for email or Lambda-to-Slack notifications.
- **Cleanup Disk Filler**: After testing, remove filler files:
  ```bash
  ssh ec2-user@<your-instance> 'rm /tmp/filler_*'
  ```
- **Optional Retries**: Configure Step Function retry policies on the SSM send-command step for transient agent issues.