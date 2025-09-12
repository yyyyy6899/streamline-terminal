#!/bin/bash
set -e

CONFIG_DIR=${1:-$(pwd)/config}
mkdir -p "$CONFIG_DIR"

if docker ps -a --format '{{.Names}}' | grep -Eq "^brave$"; then
  echo "Removing existing brave container..."
  docker rm -f brave
fi

echo "Building Docker image..."
docker build -t brave-browser .

echo "Running Brave container..."
docker run -d \
  --name brave \
  -e PUID=1000 \
  -e PGID=1000 \
  -e TZ=Etc/UTC \
  -p 3000:3000 \
  -p 3001:3001 \
  -v "$CONFIG_DIR:/config" \
  --shm-size="1gb" \
  --restart unless-stopped \
  brave-browser

echo "✅ Brave browser container is running."
