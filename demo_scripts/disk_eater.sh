#!/bin/bash
# disk_eater.sh - fill root filesystem incrementally until >=95% usage
set -euo pipefail
echo "Starting disk fill to reach >=95% usage on '/'."
counter=0
while true; do
  # get percent used without the percent sign
  used=$(df --output=pcent / | tail -1 | tr -dc '0-9')
  echo "Current usage: ${used}%"
  if [ "${used}" -ge 95 ]; then
    echo "Reached ${used}% usage. Stopping disk fill."
    break
  fi
  # create a 50MB filler file
  dd if=/dev/zero of=/tmp/filler_${counter}.bin bs=5M count=10 &> /dev/null
  counter=$((counter + 1))
done
echo "Disk eater finished."