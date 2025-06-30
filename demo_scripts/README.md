# RootGuard Demo Instructions

1. Deploy CloudWatch Agent with the provided config.
2. Set up an alarm for disk usage > 90%.
3. Configure EventBridge with the included rule to trigger the EBSGrowStepTrigger Lambda.
4. The Lambda will start the Step Function that:
   - Fetches the EBS volume ID
   - Increases the volume size
   - Expands the file system
5. Use `fallocate -l 1G dummyfile` to simulate disk usage on EC2.
6. Verify expansion with `df -h`.
