#!/bin/bash
set -e

sleep 15

# Loop through each service and check if it is up
for service in $(docker-compose config --services); do
  state=$(docker-compose ps -q "$service" | xargs docker inspect -f '{{.State.Status}}')
  if [ "$state" != "running" ]; then
    echo "Service $service is not running"
    docker-compose logs "$service"
    exit 1
  fi
done

# If all services are up, exit with success code
echo "All services are up"
exit 0
