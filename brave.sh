#!/bin/bash
set -e

echo "✅ Starting Brave container with /config mounted..."

# Start Brave browser (inherited CMD from base image, or launch X server etc.)
# Since LinuxServer Brave auto-starts, just exec to hold the container open
exec sleep infinity
